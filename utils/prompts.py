import random

__all__ = ["prompts", "random_prompt"]

def prompts():
    return {
        "photorealistic": "Emphasize a high level of realism in the image, capturing intricate details, accurate lighting, and lifelike textures",
        "semantic": "Ensure that the image accurately represents the intended meaning and context of the subject and the chosen environment",
        "coherence": "Maintain a logical and coherent composition, ensuring that the elements within the image seamlessly blend together to create a visually harmonious scene",
        "novelty": "Aim for a unique and original depiction, showcasing a fresh and distinctive perspective"
    }


def random_prompt(selected_model):
    prompts = {
        "model-1": [
            "redshift style incredible highly detailed space ship, space background, perfect composition, ...",
            "arcane style dublex, redshift style, What went wrong digital artwork concept art ...",
            "My heart is an ocean, fantasy art, cinema 4d, matte painting, polished, beautiful, colorful, ..."
        ],
        "model-2": [
            "Ode to Neon': Ultra-modern duplex design, Octane render, high-res, iridescent, metallic accents, ..."
        ],
        "model-3": [
            "Nocturnal 2100: Mysterious Metropolis, blend of glass, metal, and vibrant neon, exquisitely detailed, ..."
        ],
        "model-4": [
            "hyperpunk 2100::1, pagani zonda, octane render,4k, volumetric lighting, unreal engine, ..."
        ]
    }

    if selected_model in prompts:
        return random.choice(prompts[selected_model])
    else:
        return None