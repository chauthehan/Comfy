import os
import random
import sys
from typing import Sequence, Mapping, Any, Union
import torch


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    """Returns the value at the given index of a sequence or mapping.

    If the object is a sequence (like list or string), returns the value at the given index.
    If the object is a mapping (like a dictionary), returns the value at the index-th key.

    Some return a dictionary, in these cases, we look for the "results" key

    Args:
        obj (Union[Sequence, Mapping]): The object to retrieve the value from.
        index (int): The index of the value to retrieve.

    Returns:
        Any: The value at the given index.

    Raises:
        IndexError: If the index is out of bounds for the object and the object is not a mapping.
    """
    try:
        return obj[index]
    except KeyError:
        return obj["result"][index]


def find_path(name: str, path: str = None) -> str:
    """
    Recursively looks at parent folders starting from the given path until it finds the given name.
    Returns the path as a Path object if found, or None otherwise.
    """
    # If no path is given, use the current working directory
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        print(f"{name} found: {path_name}")
        return path_name

    # Get the parent directory
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory
    return find_path(name, parent_directory)


def add_comfyui_directory_to_sys_path() -> None:
    """
    Add 'ComfyUI' to the sys.path
    """
    comfyui_path = find_path("ComfyUI")
    if comfyui_path is not None and os.path.isdir(comfyui_path):
        sys.path.append(comfyui_path)
        print(f"'{comfyui_path}' added to sys.path")


def add_extra_model_paths() -> None:
    """
    Parse the optional extra_model_paths.yaml file and add the parsed paths to the sys.path.
    """
    try:
        from main import load_extra_path_config
    except ImportError:
        print(
            "Could not import load_extra_path_config from main.py. Looking in utils.extra_config instead."
        )
        from utils.extra_config import load_extra_path_config

    extra_model_paths = find_path("extra_model_paths.yaml")

    if extra_model_paths is not None:
        load_extra_path_config(extra_model_paths)
    else:
        print("Could not find the extra_model_paths config file.")


add_comfyui_directory_to_sys_path()
add_extra_model_paths()


def import_custom_nodes() -> None:
    """Find all custom nodes in the custom_nodes folder and add those node objects to NODE_CLASS_MAPPINGS

    This function sets up a new asyncio event loop, initializes the PromptServer,
    creates a PromptQueue, and initializes the custom nodes.
    """
    import asyncio
    import execution
    from nodes import init_extra_nodes
    import server

    # Creating a new event loop and setting it as the default loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Creating an instance of PromptServer with the loop
    server_instance = server.PromptServer(loop)
    execution.PromptQueue(server_instance)

    # Initializing custom nodes
    init_extra_nodes()


from nodes import NODE_CLASS_MAPPINGS


def main():
    import_custom_nodes()
    with torch.inference_mode():
        string_literal = NODE_CLASS_MAPPINGS["String Literal"]()
        string_literal_28 = string_literal.get_string(
            string="Tok is wrapped up like a cozy snowman, with a soft white knitted outfit giving him a round, bundled-up appearance. He wears a snug white beanie with a fluffy pom-pom on top and a bright red knitted scarf tied around his neck. Tok's face has a peaceful. He is resting on a plush, cream-colored blanket. Beside him lies a handmade candy cane wrapped in soft white fabric with red stripes and a red bow. The overall scene is warm, soft, and festive, with a dreamy, holiday-inspired atmosphere. The quality of the image is high."
        )
        # string_literal_28 = string_literal.get_string(
        #     string="Tok is wrapped in a soft, cream-colored swaddle, resting on a plush, curly-textured blanket. She wears a delicate floral headband made of white petals with subtle pearl accents. Surrounding the infant are luxury elements, including a pearl-adorned necklace with gold details and a designer-branded ribbon, creating a sophisticated and high-end aesthetic. The backdrop features a black Chanel-inspired theme, adding contrast to the soft, angelic tones of the baby’s outfit and accessories."
        # )
        # string_literal_28 = string_literal.get_string(
        #     string="Tok is a baby lying on a soft, fluffy beige carpet, wrapped in a pink towel with a matching towel wrapped around her head like a turban. She holds a makeup brush or lipstick, appearing curious and playful. Surrounding tok are various beauty products, including makeup brushes, a compact mirror, an eyeshadow palette, a curling iron, a smartphone, and nail polish. The setting looks cozy and warm, with soft lighting and a fun, humorous tone."
        # )
        # string_literal_28 = string_literal.get_string(
        #     string="Tok is a newborn baby wrapped snugly in a soft, knitted green blanket with a red trim around the neckline. A large, flowing red bow made of a fuzzy fabric is tied around Tok’s body, draping down with its long ends extending outward. The bow is voluminous, adding to the festive aesthetic. Above Tok, an elegant Christmas wreath is arranged in a semicircle. The wreath consists of lush green pine branches, deep brown pinecones, and clusters of bright red berries, creating a rich and textured appearance. The background is a deep, muted green, which enhances the holiday ambiance and contrasts beautifully with Tok’s red and green wrapping"
        # )
        # string_literal_28 = string_literal.get_string(
        #     string="Tok is positioned inside a rustic wooden bucket, lined with a soft brown cushion that cradles him. He is sleeping. He is wearing a handmade knitted hat with bear ears, blending seamlessly with his surroundings. Tok is surrounded by a variety of plush teddy bears in different shades of brown, beige, and cream. The teddy bears vary in texture and size, some appearing well-loved with slightly matted fur, while others are fluffier. The background is a smooth, warm-toned brown surface that complements the cozy and harmonious setup. The lighting is soft and even, casting a gentle glow on Tok and the plush toys, creating a serene composition."
        # )
        # string_literal_28 = string_literal.get_string(
        #     string="Tok is dressed in a knitted rust-colored outfit with matching pants, a long-sleeved top, and a hat featuring round ears, resembling a small animal. Tok is seated in a rustic wooden basket lined with soft, textured fabric in earthy tones. He is sleeping. Behind Tok, there is a fluffy beige fur-like cushion that creates a mane-like effect. The basket is surrounded by loosely woven green and beige knitted blankets that spill onto a dark wooden floor. The setup has a cozy, nature-inspired aesthetic with warm, earthy tones complementing the wooden background.The lighting appears to be diffused, likely from a softbox or natural light source, ensuring an even glow without harsh highlights. This creates a cozy and professional studio-like ambiance, emphasizing the warm, rustic aesthetic of the setup."
        # )

        # string_literal_28 = string_literal.get_string(
        #      string="Tok is a newborn wrapped in yellow like a chick, giving him a round, bundled appearance.
# He is sleeping. He is wearing a matching hat with orange and green details, resembling a fruit, tied under his chin with an orange string.

# Tok is lying on a beige surface with a plush, quilted peanut-shaped pillow supporting his head. Beside Tok, there is a plush toy with a white body and orange accents, resembling a stylized animal with teal eyes and an orange fruit-like detail on its head. A small, separate plush peanut is also near Tok. The quality of the image is high. and it's a top-view image."
        # )
        checkpointloadersimple = NODE_CLASS_MAPPINGS["CheckpointLoaderSimple"]()
        checkpointloadersimple_74 = checkpointloadersimple.load_checkpoint(
            ckpt_name="flux1-dev-fp8.safetensors"
        )

        cliptextencode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
        cliptextencode_6 = cliptextencode.encode(
            text=get_value_at_index(string_literal_28, 0),
            clip=get_value_at_index(checkpointloadersimple_74, 1),
        )

        ksamplerselect = NODE_CLASS_MAPPINGS["KSamplerSelect"]()
        ksamplerselect_16 = ksamplerselect.get_sampler(sampler_name="euler")

        randomnoise = NODE_CLASS_MAPPINGS["RandomNoise"]()
        randomnoise_25 = randomnoise.get_noise(noise_seed=random.randint(1, 2**64))

        int_literal = NODE_CLASS_MAPPINGS["Int Literal"]()
        int_literal_70 = int_literal.get_int(int=1024)

        int_literal_71 = int_literal.get_int(int=1024)

        loraloadermodelonly = NODE_CLASS_MAPPINGS["LoraLoaderModelOnly"]()
        loraloadermodelonly_72 = loraloadermodelonly.load_lora_model_only(
            lora_name="ban_chi_hai_1_flux_lora_v1_000001750.safetensors",
            strength_model=1.1,
            model=get_value_at_index(checkpointloadersimple_74, 0),
        )

        emptylatentimage = NODE_CLASS_MAPPINGS["EmptyLatentImage"]()
        modelsamplingflux = NODE_CLASS_MAPPINGS["ModelSamplingFlux"]()
        fluxguidance = NODE_CLASS_MAPPINGS["FluxGuidance"]()
        basicguider = NODE_CLASS_MAPPINGS["BasicGuider"]()
        basicscheduler = NODE_CLASS_MAPPINGS["BasicScheduler"]()
        samplercustomadvanced = NODE_CLASS_MAPPINGS["SamplerCustomAdvanced"]()
        vaedecode = NODE_CLASS_MAPPINGS["VAEDecode"]()
        saveimage = NODE_CLASS_MAPPINGS["SaveImage"]()

        for q in range(1):
            emptylatentimage_5 = emptylatentimage.generate(
                width=get_value_at_index(int_literal_70, 0),
                height=get_value_at_index(int_literal_71, 0),
                batch_size=1,
            )

            modelsamplingflux_61 = modelsamplingflux.patch(
                max_shift=1.15,
                base_shift=0.5,
                width=get_value_at_index(int_literal_70, 0),
                height=get_value_at_index(int_literal_71, 0),
                model=get_value_at_index(loraloadermodelonly_72, 0),
            )

            fluxguidance_60 = fluxguidance.append(
                guidance=3.5, conditioning=get_value_at_index(cliptextencode_6, 0)
            )

            basicguider_22 = basicguider.get_guider(
                model=get_value_at_index(modelsamplingflux_61, 0),
                conditioning=get_value_at_index(fluxguidance_60, 0),
            )

            basicscheduler_17 = basicscheduler.get_sigmas(
                scheduler="simple",
                steps=30,
                denoise=1,
                model=get_value_at_index(modelsamplingflux_61, 0),
            )

            samplercustomadvanced_13 = samplercustomadvanced.sample(
                noise=get_value_at_index(randomnoise_25, 0),
                guider=get_value_at_index(basicguider_22, 0),
                sampler=get_value_at_index(ksamplerselect_16, 0),
                sigmas=get_value_at_index(basicscheduler_17, 0),
                latent_image=get_value_at_index(emptylatentimage_5, 0),
            )

            vaedecode_8 = vaedecode.decode(
                samples=get_value_at_index(samplercustomadvanced_13, 0),
                vae=get_value_at_index(checkpointloadersimple_74, 2),
            )

            saveimage_77 = saveimage.save_images(
                filename_prefix="ComfyUI", images=get_value_at_index(vaedecode_8, 0)
            )


if __name__ == "__main__":
    main()
