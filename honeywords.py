import random

from llm import generate_response
from llm.logger import logger


def generate_honey_words(dataset: str, temperature: int, password: str):
    logger.info(f"Starting honey word generation for dataset: {dataset} with temperature: {temperature}")
    with open(f"dataset/{dataset}.txt", "r") as f:
        data = f.readlines()
    for line in data:
        line = line.replace(" ", "").replace("\n", "")
        response = generate_response(
            prompt=f"Suggest 19 decoy passwords for the original password: '{password}', that are similar to '{line}'. Each password should be  distinct from the others while still reflecting a core pattern of the original password. Must only output 19 passwords, separate each password with a new comma. Follow the rule and provide only one line of output, do not print disclaimer messages or similar messages like that.",
            kwargs={
                "temperature": temperature,
            },
        )
        response_list = response.split(",")
        response_list.append(password)
        random.shuffle(response_list)

        return [response_list, response_list.index(password)]