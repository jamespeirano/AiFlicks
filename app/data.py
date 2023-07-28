# Plans data
PLANS = {
    'Free': {
        'price': 0,
        'features': ['Unlimited image generations', 'Save your images', '5 models to choose from']
    },
    'Basic': {
        'price': 3,
        'features': [
            'Unlimited image generations',
            'Save your images',
            '10+ models to choose from',
            'Enhance and expand your images',
            'Prompt to image guided generation'
        ]
    },
    'Pro': {
        'price': 7,
        'features': [
            'Unlimited image generations',
            'Save your images',
            '20+ models to choose from',
            'Access to new models',
            'Prioritized access to new features',
            'Early access to improvements'
        ]
    },
}

PLAN_PRICES = {
    'Free': 0,
    'Basic': 3,
    'Pro': 7,
}

# Models data
MODELS = [
    {
        'title': 'Stable Vision V15',
        'name' : 'stable-diffusion-v15',
        'description': 'Elevate your creations with a perfect blend of stability and creativity. With Stable Vision, watch your ideas transform into crystal clear, mesmerizing visuals.',
        'is_free': True,
    },
    {
        'title': 'Next Gen Render v21',
        'name' : 'stable-diffusion-v21',
        'description': 'Step into the future of image rendering with Next Gen Render. Your wildest imaginations seamlessly become stunning, photorealistic masterpieces.',
        'is_free': True,
    },
    {
        'title': 'Next Gen Render XL Base',
        'name' : 'stable-diffusion_xl_base',
        'description': 'Step into the future of image rendering with Next Gen Render. Your wildest imaginations seamlessly become stunning, photorealistic masterpieces.',
        'is_free': True,
    },
    {
        'title': 'Dream Portray PhotoReal',
        'name' : 'dreamlike-photo-real',
        'description': 'Experience the magic where dreams meet reality. Dream Portray PhotoReal renders your imagination into dreamlike images, adding a touch of photorealistic charm.',
        'is_free': True,
    },
    {
        'title': 'Dreams To Life',
        'name' : 'dream-shaper',
        'description': 'Bring your dreams to life with Dreams To Life. Sculpt, mold, and transform your imaginations into dynamic, vivid images.',
        'is_free': True,
    },
    {
        'title': 'Vivid Reality v14',
        'name' : 'realistic-vision-v14',
        'description': 'Witness the birth of your imaginations in high definition. With Vivid Reality, your thoughts turn into striking, photorealistic visuals.',
        'is_free': True,
    },
    {
        'title': 'Anime Craft Nitro',
        'name' : 'nitro-diffusion',
        'description': 'Fast-track your creativity with Anime Craft Nitro. Create dynamic, energetic anime visuals that capture the speed of your imagination.',
        'is_free': True,
    },
    {
        'title': 'Anime Fantasy Maker',
        'name' : 'dreamlike-anime',
        'description': 'Unleash your fantasies into the world of anime. Anime Fantasy Maker converts your thoughts into vibrant and dreamlike anime images.',
        'is_free': False,
    },
    {
        'title': 'Limitless Artistry v5',
        'name' : 'anything-v5',
        'description': 'Transform every thought into an artful masterpiece. With Limitless Artistry, you have the freedom to create any and all visuals you can dream of.',
        'is_free': True,
    }
]


PROMPTS = {
    "stable-diffusion": [
        {"prompt": "A tranquil, serene lake at sunset with hues of oranges, purples, and pinks reflecting off the still water", 
        "negative_prompt": "A crowded, noisy urban cityscape at midday"},
        {"prompt": "A breathtaking mountainous landscape in spring with blooming wildflowers and snowcapped peaks", 
        "negative_prompt": "A flat, barren desert devoid of any life"},
        {"prompt": "An enchanting forest filled with autumn leaves of fiery reds, oranges, and yellows", 
        "negative_prompt": "A monotonous, plain beach with no vegetation"},
        {"prompt": "A quaint snow-covered village tucked away in the mountains, smoke spiraling up from chimneys", 
        "negative_prompt": "A hot, humid tropical jungle teeming with insects"},
        {"prompt": "An underwater spectacle featuring a vibrant coral reef bustling with colorful marine life", 
        "negative_prompt": "A concrete skyline crowded with dull, gray skyscrapers"},
        {"prompt": "A single blossoming cherry tree in full bloom, its petals falling like snowflakes on a quiet pond", 
        "negative_prompt": "An industrial site filled with machines and devoid of natural beauty"},
        {"prompt": "A majestic waterfall cascading into a crystal-clear pool, surrounded by lush greenery", 
        "negative_prompt": "A bustling, dirty subway station during rush hour"},
        {"prompt": "Rolling hills covered in lush green meadows under a clear blue sky dotted with white, fluffy clouds", 
        "negative_prompt": "A concrete parking lot filled with cars and devoid of greenery"},
        {"prompt": "A starry night sky, the Milky Way stretching across the horizon, above a tranquil, moonlit lake", 
        "negative_prompt": "A gray office building under the harsh light of the midday sun"},
        {"prompt": "A double rainbow arching over a verdant field, golden sunlight illuminating the landscape after a storm", 
        "negative_prompt": "A bustling supermarket filled with artificial light and packed shelves"},
    ],
    "stable-diffusion-v21": [
        {"prompt": "A mesmerizing city skyline at night, with glowing lights reflecting off of the calm harbor waters",
        "negative_prompt": "A quiet countryside with small cottages and farmlands"},
        {"prompt": "A futuristic cityscape brimming with skyscrapers adorned with neon lights and flying cars",
        "negative_prompt": "A quiet, rustic medieval town with cobblestone streets and horse-drawn carriages"},
        {"prompt": "Neon-lit urban streets bustling with life, illuminated billboards, and a diverse crowd",
        "negative_prompt": "A quiet, solitary forest with towering trees and fallen leaves"},
        {"prompt": "A collection of abstract geometric shapes, their bright, contrasting colors creating an eye-catching visual display",
        "negative_prompt": "Realistic animals in their natural habitats"},
        {"prompt": "A busy marketplace with colorful stalls, diverse merchandise, and people haggling",
        "negative_prompt": "A lonely desert landscape with nothing but sand dunes"},
        {"prompt": "An exploration into the heart of a dense jungle, with ancient ruins overgrown with vegetation",
        "negative_prompt": "A modern architectural structure with clean lines and minimalist design"},
        {"prompt": "A stunning Art Deco design with intricate patterns, bold shapes, and vibrant colors",
        "negative_prompt": "Natural landscapes with mountains, rivers, and forests"},
        {"prompt": "An ancient temple shrouded in mystery, its stone walls adorned with intricate carvings",
        "negative_prompt": "A futuristic space station with state-of-the-art technology and minimalist interiors"},
        {"prompt": "A vibrant cityscape inspired by a cyberpunk aesthetic, complete with neon lights, dense skyscrapers, and futuristic tech",
        "negative_prompt": "A peaceful rural farm with open fields and farm animals"},
        {"prompt": "A lively scene inspired by the Roaring 1920s, with flapper dresses, jazz bands, and luxurious parties",
        "negative_prompt": "A futuristic scene with advanced technology, robots, and digital interfaces"},
    ],
    "dreamlike-photo-real": [
        {"prompt": "A fantastical scene of bioluminescent mushrooms glowing in a dense, dreamlike forest",
        "negative_prompt": "A modern cityscape bustling with traffic and crowds"},
        {"prompt": "A surreal landscape where floating islands dot the sky and waterfalls flow from clouds",
        "negative_prompt": "A normal suburban neighborhood with houses and lawns"},
        {"prompt": "A dreamscape where the moon is so close that you can touch it, illuminating a tranquil sea",
        "negative_prompt": "A simple, stark, sunlit desert"},
        {"prompt": "A magical underwater world teeming with mythical sea creatures and ancient underwater ruins",
        "negative_prompt": "A crowded marketplace in a city"},
        {"prompt": "An ethereal scene where trees have leaves of brilliant gemstones and rivers flow with liquid gold",
        "negative_prompt": "An office environment with computers and paperwork"},
        {"prompt": "A whimsical winter landscape where snowflakes are the size of leaves and icicles sparkle like diamonds",
        "negative_prompt": "A hot, crowded beach during summer"},
        {"prompt": "A mesmerizing sky filled with auroras of all colors dancing above a serene, frozen landscape",
        "negative_prompt": "A dull, mundane city street"},
        {"prompt": "A fantastical jungle where giant flowers bloom and the air shimmers with iridescent butterflies",
        "negative_prompt": "A conventional living room with standard furniture"},
        {"prompt": "A dreamlike scene where clouds are made of cotton candy and rainbows are everyday phenomena",
        "negative_prompt": "A gray, rainy day in the city"},
        {"prompt": "A mystical realm where stars are within arm's reach and galaxies swirl in the night sky",
        "negative_prompt": "A busy, noisy construction site"},
    ],
    "dream-shaper": [
        {"prompt": "A celestial dream, with galaxies swirling, stars illuminating the velvet blackness, and planets hanging in the vast expanse",
        "negative_prompt": "A cluttered office space with computers, paperwork, and office chairs"},
        {"prompt": "A dreamlike landscape where mountains touch the clouds, valleys bloom with mystical flowers, and rivers shimmer with magical light",
        "negative_prompt": "A mundane suburban neighborhood with identical houses"},
        {"prompt": "A fantastical scene where mythical creatures roam freely in a lush, vibrant forest of gigantic trees and glowing plants",
        "negative_prompt": "A bustling city street during rush hour"},
        {"prompt": "A serene dreamscape of a beach with rainbow-colored sand, azure waters, and a sky painted with sunset hues",
        "negative_prompt": "A grey, cold, industrial factory environment"},
        {"prompt": "A dream of an ancient civilization thriving in harmony with nature, with elaborate structures made from giant mushrooms and crystal clear waterfalls",
        "negative_prompt": "A modern-day shopping mall filled with shops and people"},
        {"prompt": "A whimsical wonderland where oversized flora and fauna create a surreal but beautiful ecosystem",
        "negative_prompt": "A standard classroom with desks, chairs, and a blackboard"},
        {"prompt": "A surreal cityscape where buildings float on fluffy clouds and bridges of light connect them",
        "negative_prompt": "A typical countryside with farms and fields"},
        {"prompt": "A dreamlike portrait of an elegant, mythical creature against a backdrop of a mesmerizing twilight sky",
        "negative_prompt": "A crowded bus station during peak hours"},
        {"prompt": "A dreamscape where the sea and sky merge seamlessly, with marine life swimming freely in the sky and clouds floating gently on the sea",
        "negative_prompt": "A generic kitchen with standard appliances and fixtures"},
        {"prompt": "A vision of a tranquil garden in spring bloom, with trees sprouting blossoms of pure light and petals made of liquid gold",
        "negative_prompt": "A traffic-jammed highway in the city"},
    ],
    "realistic-vision-v14": [
        {"prompt": "A panoramic view of a beautiful mountain range, with the rising sun painting the sky with hues of orange and pink",
        "negative_prompt": "A crowded, bustling cityscape filled with skyscrapers and traffic"},
        {"prompt": "A majestic and intricate medieval castle standing atop a lush hill under a clear blue sky",
        "negative_prompt": "A modern-day city with contemporary architecture"},
        {"prompt": "A vibrant coral reef teeming with a diverse array of colorful, tropical fish and marine life",
        "negative_prompt": "A dry, barren desert with no sign of life"},
        {"prompt": "A lush, tranquil rainforest with a hidden waterfall cascading down a rocky cliff into a serene pool",
        "negative_prompt": "An industrial site with factories and smokestacks"},
        {"prompt": "A peaceful countryside scene of rolling green hills, blooming wildflowers, and a quaint farmhouse",
        "negative_prompt": "A bustling city street with neon lights and billboards"},
        {"prompt": "A romantic view of Paris with the Eiffel Tower in the backdrop, bathed in the warm light of the setting sun",
        "negative_prompt": "A dense, dark forest with tangled branches"},
        {"prompt": "An ethereal northern lights (aurora borealis) display, dancing across the dark night sky above a tranquil, snowy landscape",
        "negative_prompt": "A crowded, noisy marketplace"},
        {"prompt": "A quiet, peaceful beach with soft white sand, turquoise waters, and a single palm tree providing shade",
        "negative_prompt": "A busy airport filled with travelers"},
        {"prompt": "A beautiful cherry blossom (sakura) tree in full bloom, petals falling gently onto a traditional Japanese stone garden",
        "negative_prompt": "A modern, urban scene with skyscrapers and traffic"},
        {"prompt": "An idyllic Mediterranean village with white-washed houses, blue-domed churches, and cobblestone streets overlooking the sea",
        "negative_prompt": "A noisy, industrial construction site"},
    ],
    "nitro-diffusion": [
        {"prompt": "A magical girl with twinkling eyes, flowing hair, and a frilly dress, holding a sparkling wand against a starry night sky",
        "negative_prompt": "A mundane, modern-day office scene"},
        {"prompt": "An epic anime scene where a heroic knight in intricate armor confronts a fiery dragon in a dramatic, rocky landscape",
        "negative_prompt": "A peaceful countryside with farms and animals"},
        {"prompt": "A serene school rooftop scene in spring, with students enjoying lunch amid a shower of cherry blossom petals",
        "negative_prompt": "A bustling city street with traffic and tall buildings"},
        {"prompt": "A mythical creature gracefully soaring through the clouds over a beautiful fantasy city",
        "negative_prompt": "A common household scene with furniture and appliances"},
        {"prompt": "A romantic anime scene under a sky filled with shooting stars, with a couple holding hands and making wishes",
        "negative_prompt": "A dull, gray, industrial factory scene"},
        {"prompt": "A chibi character with exaggerated features joyfully eating a huge ice-cream under a bright summer sky",
        "negative_prompt": "A realistic, dark, and moody woodland"},
        {"prompt": "An anime-style grand library filled with endless rows of ancient books, magical artifacts, and a wizard studying spells",
        "negative_prompt": "A mundane, cluttered office environment"},
        {"prompt": "An anime character summoning a powerful spirit creature in a dynamic action scene full of energy and vibrant colors",
        "negative_prompt": "A calm and quiet beach with only sand and sea"},
        {"prompt": "A group of anime friends sharing a fun-filled moment in a lively cityscape with neon lights and billboards",
        "negative_prompt": "A peaceful countryside with farmlands and a setting sun"},
        {"prompt": "A mystical forest scene featuring an anime fairy with glistening wings, surrounded by glowing flowers and magical creatures",
        "negative_prompt": "A busy, modern-day market place with people and merchandise"},
    ],
    "dreamlike-anime": [
        {"prompt": "A mystic guardian overlooking an ancient forest, with the moonlight filtering through the dense foliage",
        "negative_prompt": "A busy, modern city street with cars and skyscrapers"},
        {"prompt": "An anime character with flowing, ethereal hair standing at the edge of a dreamlike sea under a star-filled sky",
        "negative_prompt": "A standard school classroom scene with desks and chalkboard"},
        {"prompt": "An enchanted library filled with magical books, floating quills, and glowing orbs of light",
        "negative_prompt": "A mundane suburban neighborhood with lawns and houses"},
        {"prompt": "A group of magical creatures having a feast in a hidden glade, surrounded by luminous plants and crystalline structures",
        "negative_prompt": "A crowded shopping mall with people and merchandise"},
        {"prompt": "An anime knight in gleaming armor, standing atop a hill with a dragon-shaped constellation illuminating the night sky",
        "negative_prompt": "A simple, empty desert landscape"},
        {"prompt": "An anime-inspired cherry blossom festival, with characters enjoying the view, colorful stalls, and lanterns floating in the night sky",
        "negative_prompt": "A busy construction site with heavy machinery and workers"},
        {"prompt": "A whimsical anime city where buildings are made from oversized candy and streets are rivers of chocolate",
        "negative_prompt": "A modern, minimalist architectural structure"},
        {"prompt": "A spirited anime character commanding the elements in an epic showdown on top of a floating island",
        "negative_prompt": "A quiet, conventional living room setting"},
        {"prompt": "A tranquil anime scene depicting a serene lake with water lilies, willow trees, and a traditional Japanese tea house",
        "negative_prompt": "A chaotic, noisy urban environment with traffic and billboards"},
        {"prompt": "A dreamlike anime depiction of a bustling festival in a world where mythical creatures and humans coexist",
        "negative_prompt": "A monotonous office setting with cubicles and computers"},
    ],
    "anything-v5": [
        {"prompt": "An otherworldly landscape with floating islands, waterfalls in the sky, and a castle made of clouds",
        "negative_prompt": "A typical office setting with computers and desks"},
        {"prompt": "A vibrant and bustling market scene in a futuristic cyberpunk city with neon lights and holograms",
        "negative_prompt": "A tranquil countryside landscape with fields and pastures"},
        {"prompt": "An ethereal underwater city with mermaids, glowing corals, and mythical sea creatures",
        "negative_prompt": "A barren desert landscape under the scorching sun"},
        {"prompt": "A fantastical forest scene with giant mushrooms, fairy folk, and a pathway of glowing pebbles",
        "negative_prompt": "A modern industrial factory with machines and smokestacks"},
        {"prompt": "A surreal depiction of the Parisian skyline, with hot air balloons and winged creatures filling the sky",
        "negative_prompt": "A normal suburban neighborhood with cars and houses"},
        {"prompt": "A grand medieval feast taking place in an intricately designed great hall filled with lords, ladies, and entertainers",
        "negative_prompt": "A standard classroom scene with students and a teacher"},
        {"prompt": "An idyllic beach scene at sunset, with sea creatures playing in the waves, and palm trees swaying to the rhythm of the ocean breeze",
        "negative_prompt": "A bustling city scene during rush hour"},
        {"prompt": "A dreamlike botanical garden teeming with luminous plants, fluttering butterflies, and a treehouse in the center",
        "negative_prompt": "A simple, empty room with white walls and a wooden floor"},
        {"prompt": "A mesmerizing space scene with vibrant nebulas, swirling galaxies, and a space station in the foreground",
        "negative_prompt": "A standard kitchen scene with cooking utensils and appliances"},
        {"prompt": "A charming winter scene in a magical realm, with glistening ice palaces, snow fairies, and reindeer-drawn sleighs",
        "negative_prompt": "A busy, noisy construction site"},
    ]
}