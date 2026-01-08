import aiohttp
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin

from ..config import settings
from ..models.user_content import UserContentPydantic


class ScraperService:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def scrape_blog(self) -> List[UserContentPydantic]:
        """Scrape blog posts from configured URL."""
        if not settings.blog_url:
            return []

        items = []
        try:
            async with self.session.get(settings.blog_url) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Generic scraping: look for article tags or common post selectors
                    posts = (
                        soup.find_all("article")
                        or soup.find_all(class_="post")
                        or soup.find_all("div", class_="entry")
                    )

                    for post in posts[:10]:  # Limit to 10 for demo
                        title_tag = post.find("h1") or post.find("h2") or post.find("a")
                        title = title_tag.get_text().strip() if title_tag else "Untitled"

                        link_tag = post.find("a")
                        url = (
                            urljoin(settings.blog_url, link_tag["href"])
                            if link_tag
                            else settings.blog_url
                        )

                        content = post.get_text().strip()[:500]  # Snippet

                        item = UserContentPydantic(
                            source="blog",
                            url=url,
                            title=title,
                            content=content,
                            summary=content[:200] + "..." if len(content) > 200 else content,
                        )
                        items.append(item)
        except Exception as e:
            print(f"Error scraping blog: {e}")

        return items

    async def scrape_github(self) -> List[UserContentPydantic]:
        """Scrape GitHub repos and READMEs."""
        if not settings.github_username:
            return []

        items = []
        try:
            # Get repos
            repos_url = f"https://api.github.com/users/{settings.github_username}/repos"
            async with self.session.get(repos_url) as resp:
                if resp.status == 200:
                    repos = await resp.json()
                    for repo in repos[:5]:  # Limit to 5
                        readme_url = f"https://api.github.com/repos/{settings.github_username}/{repo['name']}/readme"
                        async with self.session.get(
                            readme_url, headers={"Accept": "application/vnd.github.v3.raw"}
                        ) as readme_resp:
                            readme_content = (
                                await readme_resp.text() if readme_resp.status == 200 else ""
                            )

                            item = UserContentPydantic(
                                source="github",
                                url=repo["html_url"],
                                title=repo["name"],
                                content=readme_content,
                                summary=repo["description"] or readme_content[:200],
                            )
                            items.append(item)
        except Exception as e:
            print(f"Error scraping GitHub: {e}")

        return items

    async def scrape_all(self) -> List[UserContentPydantic]:
        """Scrape both blog and GitHub."""
        blog_items = await self.scrape_blog()
        github_items = await self.scrape_github()
        return blog_items + github_items
