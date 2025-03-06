import aiohttp
from bs4 import BeautifulSoup


class DnDParser:
    @staticmethod
    async def get_spell(name: str) -> dict:
        """Получение информации о заклинании."""
        url = f"https://dnd.su/spells/?search={name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")

                spell = {}
                spell['name'] = soup.find("h1").text.strip()
                spell['description'] = soup.find("div", class_="spell-description").text.strip()

                # Дополнительные поля
                details = soup.find_all("div", class_="spell-detail")
                for detail in details:
                    key = detail.find("span", class_="detail-label").text.strip().lower()
                    value = detail.find("span", class_="detail-value").text.strip()
                    spell[key] = value

                return spell

    @staticmethod
    async def get_class(name: str) -> dict:
        """Получение информации о классе."""
        url = f"https://dnd.su/classes/?search={name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")

                class_info = {}
                class_info['name'] = soup.find("h1").text.strip()
                class_info['description'] = soup.find("div", class_="class-description").text.strip()

                return class_info
