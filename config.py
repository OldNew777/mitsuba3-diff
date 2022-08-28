import os
from os.path import join, dirname, realpath

RES_SCENE_DIR = realpath(join(dirname(__file__), 'scenes'))
DIFF_SCENE_DIR = realpath(join(dirname(__file__), 'scenes'))
OUTPUT_DIR = realpath(join(DIFF_SCENE_DIR, '../outputs'))

CBOX_PARAM_NAMES = [
    'red.reflectance.value',
    'white.reflectance.value',
    'green.reflectance.value',
    'box.reflectance.value',
]

STAIRCASE_PARAM_NAMES = [
    'Painting1BSDF.brdf_0.reflectance.data',
    'Painting2BSDF.brdf_0.reflectance.data',
    'Painting3BSDF.brdf_0.reflectance.data',
    'WallpaperBSDF.brdf_0.reflectance.data',
]

CONFIGS = {
    'cbox-rgb': {
        'scene': join(RES_SCENE_DIR, 'cbox/cbox-rgb-initial.xml'),
        'ref_scene': join(RES_SCENE_DIR, 'cbox/cbox-rgb.xml'),
        'ref': join(RES_SCENE_DIR, 'cbox/cbox-rgb-ref.exr'),
        'params': CBOX_PARAM_NAMES,
        'scene_params': {
            'max_depth': 8,
            'rr_depth': 2,
        },
        'ref_scene_params': {
            'max_depth': 8,
            'rr_depth': 2,
        },
        'max_iterations': 100,
        'ref_spp': 1024,
        'forward_spp': 32,
        'backward_spp': 32,
    },
    'staircase': {
        'scene': join(RES_SCENE_DIR, 'staircase/scene-rgb-initial.xml'),
        'ref_scene': join(RES_SCENE_DIR, 'staircase/scene-rgb.xml'),
        'ref': join(RES_SCENE_DIR, 'staircase/scene-rgb-ref.exr'),
        'params': STAIRCASE_PARAM_NAMES,
        'scene_params': {
            'max_depth': 8,
            'rr_depth': 2,
        },
        'ref_scene_params': {
            'max_depth': 8,
            'rr_depth': 2,
        },
        'max_iterations': 100,
        'ref_spp': 1024,
        'forward_spp': 32,
        'backward_spp': 32,
    },
}
