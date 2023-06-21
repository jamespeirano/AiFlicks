import random

__all__ = ["generate_random_prompt", "negative_prompt"]

def generate_random_prompt(selected_model):
    prompts = {
        "stable-diffusion": [
            "Create a serene mountain landscape with (bright moon:1.5), under the (starry night sky:1.2), and (peaceful:1.3) surroundings.",
            "Illustrate a (bustling:1.4) cityscape at sunset, with (long shadows:1.3) from skyscrapers and (twinkling streetlights:1.2).",
            "Visualize a (calm:1.5) forest with a clear brook, surrounded by (diverse animals:1.4) and (lush plants:1.3).",
            "Depict a (futuristic city:1.6) on a distant planet with (unusual architecture:1.5), (flying cars:1.4), and (vibrant neon lights:1.2).",
            "Imagine a tranquil beach scene with a (hammock:1.2) between palm trees, looking out at the (crystal clear ocean:1.3) with a (stunning sunset:1.5).",
            "Visualize a detailed (medieval castle:1.3) at night, under the (bright moon:1.5), surrounded by a (dark forest:1.2).",
            "Illustrate a (remote lighthouse:1.4) on a rocky cliff during a (stormy night:1.5), with (intense waves:1.3) crashing against the rocks.",
            "Depict a (snowy mountain range:1.3) at sunrise, with (light rays:1.4) piercing through the (morning fog:1.5).",
            "Create a (peaceful:1.5) Japanese garden at dusk, with (stone lanterns:1.2), a (calm pond:1.3), and (cherry blossoms:1.4) in full bloom.",
            "Imagine an (ancient pyramid:1.3) in a desert, under the (scorching sun:1.2), surrounded by (sand dunes:1.4)."
        ],
        "realistic-vision": [
            "Visualize a (vibrant cityscape:1.5) at night, complete with (twinkling lights:1.4), (towering skyscrapers:1.3), and a (dazzling neon glow:1.6).",
            "Illustrate an (ancient castle:1.5) nestled atop a (lush green hill:1.4), with a (blue sky:1.3) filled with (fluffy clouds:1.2) in the background.",
            "Create a deep (ocean scene:1.6), featuring a (coral reef:1.5) teeming with (colorful marine life:1.4), and sun rays filtering through the (clear blue water:1.3).",
            "Picture an expansive desert under a (starry sky:1.5), with a caravan of camels traveling over the (sand dunes:1.4) under the (moonlight:1.6).",
            "Generate an image of a (snowy mountain range:1.3), with (pine trees dusted with snow:1.4), a clear river running through the valley, and the (Northern Lights:1.5) shimmering in the sky.",
            "Visualize an (aerial view:1.4) of a (bustling metropolis:1.5), with (busy streets:1.3), (high-rise buildings:1.2), and a (river:1.3) snaking through the city.",
            "Depict a (tranquil:1.5) autumn scene in a park, with a (carpet of leaves:1.4) on the ground and (warm sunlight:1.3) filtering through the trees.",
            "Create a (detailed:1.6) image of a (jungle waterfall:1.5), with (tropical birds:1.4) and (lush vegetation:1.3) around it.",
            "Picture an (ancient ruin:1.5) in a (dense forest:1.4), with (sun rays:1.6) piercing through the (tree canopy:1.3).",
            "Imagine a (mysterious cave:1.5) illuminated by (bio-luminescent fungi:1.6), with (crystal formations:1.4) and (underground river:1.3)."
        ],
        "nitro-diffusion": [
            "Visualize an (epic battle:1.5) between two (samurais:1.4) on a stone bridge over a (fast-flowing river:1.3), with (cherry blossom trees:1.6) in full bloom.",
            "Create a (lively:1.5) magic school on a (floating island:1.6), with (students on broomsticks:1.4) and (mythical creatures:1.3) roaming around.",
            "Imagine a (post-apocalyptic:1.6) Tokyo cityscape, with skyscrapers taken over by (nature:1.5), and a group of (young adventurers:1.4) standing on a rooftop.",
            "Illustrate a (tranquil scene:1.3) of a small ramen shop in a narrow alley of an (old Japanese town:1.5), with (lanterns:1.4) glowing and (snow:1.6) falling.",
            "Depict a (vibrant festival:1.6) scene filled with people in traditional attire, (food stalls:1.4), (lanterns:1.5), fireworks, and a (huge Ferris wheel:1.3) in the background.",
            "Create an image of a (mystical:1.6) forest at night, illuminated by (fireflies:1.5), with (elven structures:1.4) nestled among the trees.",
            "Imagine a (fierce duel:1.6) between two knights in a (grand throne room:1.5), under the watchful eyes of the (king and queen:1.4).",
            "Illustrate a (majestic:1.6) dragon resting on a (treasure hoard:1.5) inside a (massive cavern:1.4).",
            "Visualize a (hidden village:1.5) of tree houses connected by (rope bridges:1.4), in a (tropical jungle:1.6).",
            "Depict an (underground city:1.6) lit by (luminescent crystals:1.5), with (inhabitants:1.4) going about their daily life."
        ],
        "dreamlike-anime": [
            "(masterpiece:1.6), (best quality:1.5), extremely detailed CG, (beautiful detailed eyes:1.4), ultra-detailed, (intricate details:1.3), 8k wallpaper, elaborate features, (1girl:1.2), (multicolored hair:1.5),(blond hair:1.4), long hair, streaked hair, halo, looking at viewer, animal ears, red eyes,earring, black jacket, choker,upper body, floating hair, open jacket, night, full moon,outdoors",
            "best quality, painting, (cyberpunk anime:1.6), (intense_angle:1.5), standing, wet ((female_battle_android)), 25 years old, medium_hair, small_breast, (anger vein), ((diamond_shaped_pupils)), (looking to viewer), detailed eyes, mechanical_parts, (flush:1.3), (shimmer iridescent silver hair:1.4), motion_lines, face in focus, dim colors, HD, intridicated, ultra detailed cyberpunk rainy background, highly detailed, (by Kawase Hasui:1.3),CGSociety,ArtStation",
            "masterpiece, best quality, upper body, 1girl, looking at viewer, red hair, medium hair, purple eyes, demon horns, black coat, indoors, dimly lit",
            "Create a grand castle (floating:1.6) in the clouds, with a (majestic rainbow:1.5) connecting it to a (magical forest:1.4) below.",
            "Visualize a serene lakeside scene under a (glowing moon:1.5), where (luminous fairy-like creatures:1.6) are dancing on the water's surface.",
            "Imagine a mysterious portal (opening:1.6) in the middle of a bustling city street, revealing a vivid, enchanted garden filled with (mythical creatures:1.5).",
            "Illustrate a mystical underwater city lit by (bio-luminescent plants:1.6) and inhabited by (merpeople:1.5) and fantastical marine creatures.",
            "Draw a surreal scene of a giant cherry blossom tree glowing with (magical energy:1.6) in a forest, with tiny spirits swirling around it under the starry night sky.",
            "Visualize a (post-apocalyptic:1.6) world where nature has reclaimed cities, with (vines:1.5) growing over skyscrapers and (wild animals:1.4) roaming the streets.",
            "Imagine a young warrior standing on a cliff, overlooking a (vast kingdom:1.5) under a (dramatic sunset:1.6), with her (faithful pet:1.4) by her side."
        ]
    }

    if selected_model in prompts:
        return random.choice(prompts[selected_model])
    else:
        raise ValueError(f"Invalid model name: {selected_model}. Expected one of {list(prompts.keys())}.")


def generate_negative_prompt(selected_model):
    prompts = {
        "stable-diffusion" : "((((unrealistic:1.2, non-photorealistic:1.3, cartoonish:1.4, amateur:1.6, unrefined:1.5)))), low quality:1.3, pixelated:1.6, duplicate:1.5, unsettling:1.4, distortions:1.3, incomplete:1.2, off-proportions:1.3, cloned elements:1.5, unclear:1.4, low hydration:1.3, improper anatomy:1.2, poor composition:1.5, additional body parts:1.4, fuzzy:1.3",
        "realistic-vision" : "Non-realistic:1.5, 3d render:1.4, disfigured:1.6, bad art:1.5, abnormal:1.3, too close up:1.2, monochrome:1.5, odd colors:1.4, blurry:1.6, repelling:1.5, repeating:1.4, incomplete:1.6, body out of frame:1.5, poor quality:1.3, watermarked:1.2, grainy:1.4, duplicate:1.6, under-detailed:1.5, inappropriate:1.3, overly flashy:1.2, oversaturated:1.4, grainy:1.6, low quality:1.5, additional body parts:1.3, disjointed body parts:1.2, blurry:1.4, floating body parts:1.6, long body:1.5, repelling:1.3, poorly drawn:1.2, cut off cropped:1.4, unnatural:1.6, text:1.5, error:1.3",
        "nitro-diffusion" : "Human characters:1.5, overly simplistic:1.4, mechanical:1.6, overly stylized:1.5, moe:1.4, bad anatomy:1.6, distortions:1.5, over the top expressions:1.4, color overload:1.6, too simplistic background:1.5, repetitive themes:1.4, inappropriate:1.6, underdeveloped characters:1.5, additional body parts:1.4, over-accessorized:1.6, censored:1.5, excessive motion lines:1.4, overly detailed hair:1.6, unrealistic hair colors:1.5, unclear shading:1.4, inconsistent style:1.6, off-frame:1.5, off-model characters:1.4, bad line quality:1.6, low resolution:1.5, watermarked:1.4, poor translation:1.6, jarring CGI:1.5, cliches:1.4, cropped:1.6, low quality:1.5, exaggerated facial features:1.4, modern clothing:1.6, lack of detail:1.5, overused tropes:1.4, over-expressed emotions:1.6, badly drawn hands:1.5",
        "dreamlike-anime" : "Overly vibrant colors:1.5, cliche symbolism:1.4, overly simplistic background:1.6, overused themes:1.5, incongruent scenarios:1.4, nonsensical plot:1.6, excessive bloom:1.5, redundant characters:1.4, bad anatomy:1.6, deformations:1.5, overly exaggerated expressions:1.4, color overload:1.6, inappropriate:1.5, underdeveloped characters:1.4, additional body parts:1.6, over-accessorized:1.5, censored:1.4, excessive speed lines:1.6, overly detailed hair:1.5, unrealistic hair colors:1.4, unclear shading:1.6, inconsistent style:1.5, off-frame:1.4, off-model characters:1.6, poor line quality:1.5, low resolution:1.4, watermarked:1.6, poor translation:1.5, jarring CGI:1.4, cliches:1.6, cropped:1.5, low quality:1.4, exaggerated facial features:1.6, modern clothing:1.5, lack of detail:1.4, overused tropes:1.6, over-expressed emotions:1.5, badly drawn hands:1.4"
    }
    return prompts[selected_model]