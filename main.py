from src.di import container


def main():
    # Wire dependencies
    container.wire(modules=["src.agents", "src.services", "src.sources"])

    print("Hello from pydanticai-twitter-bot!")
    print("DI container wired successfully.")

    # Example: Get an agent
    # research_agent = container.research_agent_provider()
    # print("Agent ready:", research_agent)


if __name__ == "__main__":
    main()
