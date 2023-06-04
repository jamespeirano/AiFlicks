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
            "Visualize a serene mountain landscape under the starry night sky with a bright full moon.",
            "Illustrate a bustling cityscape at sunset, with skyscrapers casting long shadows and streetlights just starting to twinkle.",
            "Create an image of a calm forest with a clear, babbling brook running through it, surrounded by various animals and plants.",
            "Show a futuristic city on a distant planet with unusual architecture, flying cars, and vibrant neon lights.",
            "Picture a tranquil beach scene with a hammock between two palm trees, looking out at the crystal clear ocean with a stunning sunset in the background."
        ],
        "model-2": [
            "Visualize a vibrant cityscape at night, complete with twinkling lights, towering skyscrapers, and a dazzling neon glow.",
            "Illustrate an ancient castle nestled atop a lush green hill, with a blue sky filled with fluffy clouds in the background.",
            "Create an image of a deep ocean scene, featuring a coral reef teeming with colorful marine life, and sun rays filtering through the clear blue water.",
            "Picture an expansive desert under a starry sky, with a caravan of camels traveling over the sand dunes under the moonlight.",
            "Generate an image of a snowy mountain range, with pine trees dusted with snow, a clear river running through the valley, and the Northern Lights shimmering in the sky."
        ],
        "model-3": [
            "Visualize an epic battle scene between two powerful samurais on a stone bridge over a fast-flowing river, with cherry blossom trees in full bloom on both sides.",
            "Create an image of a lively magic school situated on a floating island, with students on broomsticks and mythical creatures roaming around.",
            "Imagine a post-apocalyptic Tokyo cityscape, with towering skyscrapers taken over by nature, and a group of young adventurers standing on a rooftop.",
            "Illustrate a tranquil scene of a small ramen shop nestled in a narrow alley of an old Japanese town, with lanterns glowing warmly and snow gently falling.",
            "Draw a vibrant festival scene filled with people in traditional attire, food stalls, lanterns, fireworks, and a huge, brightly-lit Ferris wheel in the background."
        ],
        "model-4": [
            "(masterpiece, best quality, extremely detailed CG, beautiful detailed eyes, ultra-detailed, intricate details:1.2), 8k wallpaper, elaborate features, (1girl, solo:1.4), (multicolored hair:1.2),(blond hair:1.2), long hair, streaked hair, halo, looking at viewer, animal ears, red eyes,earring, black jacket, choker,upper body, floating hair, open jacket, night, full moon,outdoors",
            "best quality, painting, cyberpunk anime, (intense_angle:0.6), standing, wet ((female_battle_android)), 25 years old, medium_hair, small_breast, (anger vein), ((diamond_shaped_pupils)), (looking to viewer), detailed eyes, mechanical_parts, (flush:1.3), (shimmer iridescent silver hair), motion_lines, face in focus, dim colors, HD, intridicated, ultra detailed cyberpunk rainy background, highly detailed, (by Kawase Hasui:1.3),CGSociety,ArtStation",
            "masterpiece, best quality, upper body, 1girl, looking at viewer, red hair, medium hair, purple eyes, demon horns, black coat, indoors, dimly lit",
            "Create an image of a grand castle floating in the clouds, with a majestic rainbow connecting it to a magical forest below.",
            "Visualize a serene lakeside scene under a glowing moon, where luminous fairy-like creatures are dancing on the water's surface.",
            "Imagine a mysterious portal opening in the middle of a bustling city street, revealing a vivid, enchanted garden filled with mythical creatures.",
            "Illustrate a mystical underwater city lit by bio-luminescent plants and inhabited by merpeople and fantastical marine creatures.",
            "Draw a surreal scene of a giant cherry blossom tree glowing with magical energy in a forest, with tiny spirits swirling around it under the starry night sky."
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