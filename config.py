import os
from os.path import join, dirname, realpath

SCENE_DIR = realpath(join(dirname(__file__), 'scenes'))
OUTPUT_DIR = 'D:/OldNew/LuisaRender/record/mitsuba3-diff/outputs'

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
        'scene': join(SCENE_DIR, 'cbox/cbox-rgb-initial.xml'),
        'ref_scene': join(SCENE_DIR, 'cbox/cbox-rgb.xml'),
        'ref': join(SCENE_DIR, 'cbox/cbox-rgb-ref.exr'),
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
        'scene': join(SCENE_DIR, 'staircase/scene-rgb-initial.xml'),
        'ref_scene': join(SCENE_DIR, 'staircase/scene-rgb.xml'),
        'ref': join(SCENE_DIR, 'staircase/scene-rgb-ref.exr'),
        'params': STAIRCASE_PARAM_NAMES,
        'scene_params': {
            'max_depth': 8,
            'rr_depth': 2,
        },
        'ref_scene_params': {
            'max_depth': 8,
            'rr_depth': 2,
        },
        'max_iterations': 1000,
        'ref_spp': 1024,
        'forward_spp': 512,
        'backward_spp': 512,
    },
}
