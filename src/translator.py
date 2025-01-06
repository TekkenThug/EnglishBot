from googletrans import Translator

async def translate_text(word: str) -> str:
    async with Translator() as translator:
        return (await translator.translate(word, dest='ru')).text