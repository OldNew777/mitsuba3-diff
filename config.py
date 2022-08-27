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

CONFIGS = {
    'cbox-rgb': {
        'scene': join(RES_SCENE_DIR, 'cbox/cbox-rgb-initial.xml'),
        'ref_scene': join(RES_SCENE_DIR, 'cbox/cbox-rgb.xml'),
        'ref': join(RES_SCENE_DIR, 'cbox/cbox-rgb-ref.exr'),
        'params': CBOX_PARAM_NAMES,
        'scene_params': {
            'res': 256,
            'max_depth': 8,
            'rr_depth': 2,
        },
        'ref_scene_params': {
            'res': 256,
            'max_depth': 8,
            'rr_depth': 2,
        },
        'max_iterations': 100,
        'forward_spp': 32,
        'backward_spp': 32,
    },
}
