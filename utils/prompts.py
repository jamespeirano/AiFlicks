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
            "(masterpiece, best quality, extremely detailed CG, beautiful detailed eyes, ultra-detailed, intricate details:1.2), 8k wallpaper, elaborate features, (1girl, solo:1.4), (multicolored hair:1.2),(blond hair:1.2), long hair, streaked hair, halo, looking at viewer, animal ears, red eyes,earring, black jacket, choker,upper body, floating hair, open jacket, night, full moon,outdoors",
            "best quality, painting, cyberpunk anime, (intense_angle:0.6), standing, wet ((female_battle_android)), 25 years old, medium_hair, small_breast, (anger vein), ((diamond_shaped_pupils)), (looking to viewer), detailed eyes, mechanical_parts, (flush:1.3), (shimmer iridescent silver hair), motion_lines, face in focus, dim colors, HD, intridicated, ultra detailed cyberpunk rainy background, highly detailed, (by Kawase Hasui:1.3),CGSociety,ArtStation",
            "masterpiece, best quality, upper body, 1girl, looking at viewer, red hair, medium hair, purple eyes, demon horns, black coat, indoors, dimly lit"
        ]
    }

    if selected_model in prompts:
        return random.choice(prompts[selected_model])
    else:
        return None


def negative_prompt(selected_model):
    prompts = {
        "stable-diffusion-v1-5" : "((((realistic, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime)))), cropped, worst quality, low quality, jpeg artifacts, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, out of focus, drawn, sketch",
        "Realistic_Vision_V1.4" : "Cartoon, 3d, disfigured, bad art, deformed, poorly drawn, extra limbs, close up, b&w, weird colors, blurry, ugly, tiling, poorly drawn hands, feet, face, out of frame, body out of frame, bad anatomy, blurred, watermark, grainy, signature, cut off, draft, low detail, low quality, double face, 2 faces, cropped, low-res, tiling, repetitive, plastic, doll, static, skimpy, swimwear, bikini, panties, bra, dress, lowres, disfigured, ostentatious, oversaturated, grain, low resolution, mutant, mutated, extra limb, missing limbs, blurred, floating limbs, disjointed limbs, deformed hands, out of focus, long neck, long body, disgusting, bad drawing, childish, cut off cropped, distorted, imperfect, surreal, bad hands, text, error, extra digit, fewer digits, worst quality, jpeg artifacts, signature, watermark, username, artist name, lots of hands, extra fingers, conjoined fingers, deformed fingers, old, ugly eyes, imperfect eyes, skewed eyes, unnatural face, stiff face, stiff body, unbalanced body, unnatural body, lacking body, unclear details, sticky details, low details, distorted details, ugly hands, imperfect hands, mutated hands and fingers, long body, mutation, poorly drawn, bad hands, fused hand, missing hand, disappearing arms, thigh, calf, legs, ui, missing fingers.",
        "Nitro-Diffusion" : "Human person, Chibi, mecha, super deformed, moe, bad anatomy, deformed, disproportional body, overly exaggerated expressions, oversaturated colors, simplistic background, repetitive themes, inappropriate fan service, underdeveloped characters, missing limbs, too many limbs, unnecessary accessories, censored, excessive speed lines, overly detailed hair, unrealistic hair colors, unclear shading, inconsistent style, out of frame, off-model characters, poor line art, low resolution, watermark, poor translation, jarring CGI, overused cliches, cropped, low quality, jpeg artifacts, exaggerated facial features, out-of-place modern clothing, lack of detail, overused tropes, exaggerated emotions, badly drawn hands.",
        "dreamlike-anime-1.0" : "Overly vibrant colors, cliche symbolism, simplistic background, overused themes, incongruent scenarios, nonsensical plot, excessive bloom, redundant characters, bad anatomy, deformed, disproportional body, overly exaggerated expressions, oversaturated colors, inappropriate fan service, underdeveloped characters, missing limbs, too many limbs, unnecessary accessories, censored, excessive speed lines, overly detailed hair, unrealistic hair colors, unclear shading, inconsistent style, out of frame, off-model characters, poor line art, low resolution, watermark, poor translation, jarring CGI, overused cliches, cropped, low quality, jpeg artifacts, exaggerated facial features, out-of-place modern clothing, lack of detail, overused tropes, exaggerated emotions, badly drawn hands."
    }
    return prompts[selected_model]