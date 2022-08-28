import os
import sys
from os.path import join, dirname, realpath
import time
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np
import drjit as dr
import mitsuba as mi
import matplotlib.pyplot as plt
from config import *


ref_seed = 0
train_seed = 2563893771
rerender_ref = False
save_intermediate = True


def mse(ref_image, rendered_image):
    return dr.mean(dr.sqr(rendered_image - ref_image))


def get_integrator(integrator_properties, default):
    if integrator_properties is None:
        return default
    # return mi.ad.integrators.prb.PRBIntegrator(props=integrator_properties)
    return mi.cuda_ad_rgb.PathIntegrator(props=integrator_properties)


def load_or_render_ref(config):
    ref_image_name = config['ref']
    if rerender_ref or not os.path.isfile(ref_image_name):
        spp = config['ref_spp']
        print(f'[ ] Rendering reference image at {spp}spp...')
        ref_scene_name = config['ref_scene']
        ref_scene = mi.load_file(ref_scene_name)

        print('*' * 80)
        print(ref_scene)
        print('*' * 80)

        ref_scene_params = config['ref_scene_params']
        integrator_properties = mi.Properties()
        integrator_properties['max_depth'] = ref_scene_params['max_depth']
        integrator_properties['rr_depth'] = ref_scene_params['rr_depth']
        integrator_properties['samples_per_pass'] = 4
        integrator = get_integrator(integrator_properties, ref_scene.integrator())
        print(integrator)

        ref_image = integrator.render(ref_scene, seed=ref_seed, spp=spp)
        cv2.imwrite(ref_image_name, cv2.cvtColor(np.array(ref_image), cv2.COLOR_RGB2BGR))
        print(f'[+] Saved reference image: {ref_image_name}')
    return cv2.imread(ref_image_name, cv2.IMREAD_UNCHANGED)


def save_info_csv(filename, **metadata):
    headers = metadata.keys()
    values = zip(*metadata.values())
    with open(filename, 'w') as f:
        f.write(', '.join(headers) + '\n')
        for r in values:
            f.write(', '.join([str(v) for v in r]) + '\n')


def optimize_prb(config_name):
    config = CONFIGS[config_name]
    output_dir = join(OUTPUT_DIR, config_name)
    os.makedirs(output_dir, exist_ok=True)

    forward_spp = config.get('forward_spp', 32)
    backward_spp = config.get('backward_spp', 32)
    max_iterations = config.get('max_iterations', 100)

    ref_image = load_or_render_ref(config)
    cv2.imwrite(join(output_dir, 'ref.exr'), ref_image)
    ref_image = mi.TensorXf(cv2.cvtColor(ref_image, cv2.COLOR_BGR2RGB))
    dr.disable_grad(ref_image)

    scene_name = config['scene']
    scene = mi.load_file(scene_name)
    params = mi.traverse(scene)
    param_keys = config['params']

    print('*' * 80)
    print(params)
    print(type(scene.integrator()))
    print('*' * 80)

    # opt = mi.ad.SGD(lr=10.0)
    opt = mi.ad.Adam(lr=0.05)
    for param_key in param_keys:
        opt[param_key] = params[param_key]
    params.update(opt)

    scene_params = config['scene_params']
    integrator_properties = mi.Properties()
    integrator_properties['max_depth'] = scene_params['max_depth']
    integrator_properties['rr_depth'] = scene_params['rr_depth']
    integrator_properties['samples_per_pass'] = 4
    integrator = get_integrator(integrator_properties, scene.integrator())

    # train
    metadata = {k: [] for k in ['timing', 'timings_forward', 'timings_backward', 'loss']}
    for iter_i in range(max_iterations):
        t_start = time.time()
        # forward pass
        seed = train_seed + iter_i
        with dr.suspend_grad():
            image = mi.render(scene, params=params, integrator=integrator, seed=seed, spp=forward_spp)
        t_end_forward = time.time()

        # backward pass
        dr.enable_grad(image)
        loss = mse(ref_image, image)
        dr.backward(loss)
        adjoint = dr.grad(image)
        dr.set_grad(image, 0.0)
        integrator.render_backward(scene, grad_in=adjoint, params=params, seed=seed, spp=backward_spp)
        opt.step()

        # clamp
        for param_key in param_keys:
            opt[param_key] = dr.clamp(opt[param_key], 0.0, 1.0)

        # Update the scene state to the new optimized values
        params.update(opt)
        t_end_backward = time.time()

        # save info
        metadata['loss'].append(loss[0])
        time_all = t_end_backward - t_start
        time_forward = t_end_forward - t_start
        time_backward = t_end_backward - t_end_forward
        metadata['timing'].append(time_all)
        metadata['timings_forward'].append(time_forward)
        metadata['timings_backward'].append(time_backward)

        if save_intermediate:
            output_dir = join(OUTPUT_DIR, config_name)
            fname = join(output_dir, '{:04d}.exr'.format(iter_i))
            cv2.imwrite(fname, cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

        # Track the loss between the ref image and the rendered image
        print(f"Iteration {iter_i:03d}: loss = {loss[0]:6f}, took {time_all:.03f}s", end='\r')

    print('\nOptimization complete.')
    del integrator, opt

    metadata_filename = join(OUTPUT_DIR, config_name, 'metadata.csv')
    save_info_csv(metadata_filename, **metadata)
    print(f'[+] Saved run metadata to: {metadata_filename}')

    return metadata['loss'][-1], image, metadata


if __name__ == '__main__':
    mi.set_variant('cuda_ad_rgb')

    config_name = sys.argv[1]
    optimize_prb(config_name)
