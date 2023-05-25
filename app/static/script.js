
$(document).ready(function() {
    $('#prompt').on('submit', function() {
        // Collect checkbox values
        var photorealistic = $('#photorealistic-checkbox').is(':checked');
        var semantic = $('#semantic-checkbox').is(':checked');
        var coherence = $('#coherence-checkbox').is(':checked');
        var novelty = $('#novelty-checkbox').is(':checked');

        // Set checkbox values in hidden inputs
        $('input[name="photorealistic"]').val(photorealistic);
        $('input[name="semantic"]').val(semantic);
        $('input[name="coherence"]').val(coherence);
        $('input[name="novelty"]').val(novelty);

        // Submit the form
        return true;
    });
});

function generateRandomPrompt() {
    // Make an API call to retrieve a random prompt
    // fetch('/random-prompt', {
    //     headers : {
    //         'Accept-Encoding': '*'
    //     }
    // })
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error('Failed to retrieve random prompt');
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         // Fill the textarea with the generated random prompt
    //         document.getElementById('prompt-textarea').value = data.prompt;
    //     })
    //     .catch(error => {
    //         console.log(error);
    //         // Handle the error appropriately (e.g., show an error message)
    //     });



    StableDiffusionPrompts = ["redshift style incredible highly detailed space ship, space background, perfect composition, beautiful detailed, intricate, insanely detailed, octane render, trending on artstation, artistic, photorealistic, concept art, soft natural volumetric cinematic perfect light, chiaroscuro, award winning photograph, splash of color, masterpiece, oil on canvas, Carne Griffiths, E. Abramzon, raphael, caravaggio, beeple, beksinski, giger style",
        "arcane style dublex, redshift style, What went wrong digital artwork concept art unreal engine cinematic Hyper detailed (highly detailed background) Highres iridescent metallic virtual octane render 4k UHD Splash screen (masterpiece) trending on deviantart artstation art by AI",
        "My heart is an ocean, fantasy art, cinema 4d, matte painting, polished, beautiful, colorful, intricate, eldritch, ethereal, vibrant, surrealism, surrealism, vray, nvdia ray tracing, cryengine, magical, 4k, 8k, masterpiece, crystal, romanticism",
        "hyperpunk 2100::1, pagani zonda, octane render,4k, volumetric lighting, unreal engine, retro advanced future concept design",
        "snthwve style nvinkpunk Futuristic City of steel glass and neon, Masterpiece, Intricate details, 8k, 16k UHD, concept art, Moody lighting, shadows, glimmering, volumetric, professional photography, Ray Tracing Global Illumination, Optics, Scattering, Glowing, Shadows, Rough, Shimmering, Ray Tracing, Ambient Occlusion, Anti-Aliasing, FKAA, TXAA, RTX, SSAO, Shaders, OpenGL-Shaders, GLSL-Shaders, Post Processing, Post-Production, Cell Shading, Tone",
        "Illuminated mind of the cosmos, stunning digital art, Blender, starfield background, exquisite detail, mesmerizing fractal patterns, ambient occlusion, masterpiece, oil on canvas, Dali, Escher, Beksinski, H.R. Giger style, trending on Behance, ultra-high definition 8K",
        "New Babylon: Revelations, virtual 3D render, Octane, Unreal Engine, supreme detail, atmospheric cityscape, cyberpunk ambiance, metallic structures bathed in neon light, HDR, concept art, showcased on ArtStation, 4K, 16K masterpiece",
        "My soul is a starlit sky, breathtaking fantasy scenery, Cinema 4D, enhanced with Nuke, radiant, mystical, 8K resolution, masterpiece, volumetric lighting, RTX ray tracing, magical crystal structures, echoes of romanticism, dreamlike surrealism, trending on DeviantArt",
        "Quantum fusion X:4.3, radical hoverbike design, Unreal Engine, Octane Render, 4K, volumetric lighting, advanced retro-futuristic concept, Art Nouveau inspired detail, showcased on Behance, digital masterpiece, RTX ray tracing",
        "The Dream Weaver, ethereal digital art, rich textures, Daz3D, iridescent holographic elements, hyper-detailed, 4K, featured on Pixiv, dramatic light and shadow, HDR, ray tracing, post-production enhancements, digital painting meets surrealism, a masterpiece reminiscent of Chagall's work",
        "Quantum fusion X:4.3, radical hoverbike design, Unreal Engine, Octane Render, 4K, volumetric lighting, advanced retro-futuristic concept, Art Nouveau inspired detail, showcased on Behance, digital masterpiece, RTX ray tracing",
        "Enigma of the Void, Blender masterpiece, space-themed artwork, stunning detail, beautiful composition, reminiscent of Beeple's work, volumetric lighting, ray traced, high-res 8K, trending on ArtStation, photorealistic starry background",
        "Ode to Neon': Ultra-modern duplex design, Octane render, high-res, iridescent, metallic accents, Unreal Engine, architectural concept art, trending on DeviantArt, photorealistic, masterpiece in digital design",
        "In the Heart of the Crystal Forest': Magical scenery, vibrant colors, hyper-realistic render with Nvidia ray tracing, CryEngine, 4K, 8K, intricate details, ethereal beauty, trending on ArtStation, a true digital masterpiece",
        "Retrowave Dreams': 8K, concept art, futuristic city bathed in neon, volumetric lighting, intricate detailing, digital masterpiece, glimmering skyscrapers, shadows playing off the high-gloss surfaces, showcasing the capabilities of ray tracing and ambient occlusion",
        "Nocturnal 2100: Mysterious Metropolis, blend of glass, metal, and vibrant neon, exquisitely detailed, 16K Ultra HD, moody atmospheric lighting, gleaming reflections, ray traced shadows, trending on ArtStation, ambient occlusion, anti-aliasing, RTX, SSAO, GLSL shaders, post-production touches, cinematic masterpiece."  
    ];
    model2 = [
        "Ode to Neon': Ultra-modern duplex design, Octane render, high-res, iridescent, metallic accents, Unreal Engine, architectural concept art, trending on DeviantArt, photorealistic, masterpiece in digital design"
    ];
    model3 = [
        "Nocturnal 2100: Mysterious Metropolis, blend of glass, metal, and vibrant neon, exquisitely detailed, 16K Ultra HD, moody atmospheric lighting, gleaming reflections, ray traced shadows, trending on ArtStation, ambient occlusion, anti-aliasing, RTX, SSAO, GLSL shaders, post-production touches, cinematic masterpiece."  
    ];
    model4 = ["hyperpunk 2100::1, pagani zonda, octane render,4k, volumetric lighting, unreal engine, retro advanced future concept design"
    ];


    // Get the currently selected model
    const selectedModel = document.getElementById('selected-model').value;

    let selectedArray;

    // Choose the array based on the selected model
    switch(selectedModel) {
        case 'model-1':
            selectedArray = StableDiffusionPrompts;
            break;
        case 'model-2':
            selectedArray = model2;
            break;
        case 'model-3':
            selectedArray = model3;
            break;
        case 'model-4':
            selectedArray = model4;
            break;
        default:
            console.error(`Unknown model: ${selectedModel}`);
            return;
    }

    // Pick a random prompt from the selected array
    const randomIndex = Math.floor(Math.random() * selectedArray.length);
    const randomPrompt = selectedArray[randomIndex];

    // Fill the textarea with the generated random prompt
    document.getElementById('prompt-textarea').value = randomPrompt;
}


function addToCart(name, price) {
    const selectElement = event.target.previousElementSibling;
    const selectedSize = selectElement.value;
    
    if (selectedSize === '') {
        alert('Please select a size.');
        return;
    }

    const overlayImage = document.querySelector(".overlay-image");
    // const overlayImageId = overlayImage.dataset_id; no longer necessary

    console.log("image ", overlayImage);
    console.log("image ", overlayImage.src);
    
    // Send an AJAX request to the backend server to add the item to the Python list
    // also add the image to the cart
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/add-to-cart');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert(`Item "${name}" (Size: ${selectedSize}) added to the cart!`);
        } else {
            alert('Failed to add item to the cart. Please try again.');
        }
    };

    const data = JSON.stringify({
        'name': name,
        'price': price,
        'size': selectedSize,
        'image': overlayImage.src
    });
    xhr.send(data);
}
