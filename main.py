import os
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("your_api_key")
)

MODEL = "gpt-6-luna"


# ============================================================
# AGENT INSTRUCTIONS
# ============================================================

AGENT_INSTRUCTIONS = """
You are an AI Morning Research Agent.

Your job is to research the most important AI developments
from the previous 24 hours and produce a concise morning briefing.

You have access to live web search.

IMPORTANT RULES:

1. You MUST search the web.
2. Search for AI developments from the previous 24 hours.
3. Do not rely on your training knowledge for current events.
4. Look across multiple credible sources.
5. Prefer primary sources and reputable technology/news publications.
6. Look for genuinely important developments, not just popular headlines.
7. If multiple articles describe the same underlying event, treat them
   as ONE story.
8. Do not give five articles about the same event.
9. Distinguish announcements, research releases, product launches,
   major company developments, important policy/regulatory developments,
   and significant technical breakthroughs.
10. Ignore stories that are clearly older than 24 hours.
11. Do not invent publication dates, facts, sources, or URLs.
12. If a story cannot be verified, do not present it as confirmed.
13. Select exactly five stories when five sufficiently important stories
    are available. If fewer than five genuinely important developments
    exist, say so rather than filling the list with weak stories.

For each selected story provide:

- Rank
- Headline
- Why it matters
- What happened
- Source
- Publication time/date if available
- Source URL

At the end provide a short section called:

"Why these five?"

Explain briefly what made these developments more significant
than the other relevant stories you found.

Your answer must contain clickable source citations supplied by
the web-search system.
"""


# ============================================================
# BUILD THE USER REQUEST
# ============================================================

def build_request():

    now = datetime.now(timezone.utc)

    twenty_four_hours_ago = now - timedelta(hours=24)

    return f"""
Find the five most important AI stories from the previous 24 hours.

Current UTC time:
{now.isoformat()}

The 24-hour window begins at:
{twenty_four_hours_ago.isoformat()}

Research the web rather than relying on pre-existing knowledge.

Search broadly enough to discover important developments, then
compare the results and remove duplicate events.

I want five DISTINCT developments, not five articles covering
the same event.

Return a concise morning research briefing with sources.
"""


# ============================================================
# RUN THE AGENT
# ============================================================

def run_agent():

    request = build_request()

    print("\n🤖 AI MORNING RESEARCH AGENT")
    print("=" * 60)

    print("\n📋 Request:")
    print(request)

    print("\n🌐 Starting live web research...\n")

    response = client.responses.create(

        model=MODEL,

        instructions=AGENT_INSTRUCTIONS,

        tools=[
            {
                "type": "web_search"
            }
        ],

        # We want the agent to actually search.
        tool_choice="required",

        input=request
    )

    return response


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(response):

    print("\n")
    print("=" * 60)
    print("📰 AI MORNING BRIEFING")
    print("=" * 60)

    print(response.output_text)

    print("\n")
    print("=" * 60)
    print("✅ RESEARCH COMPLETE")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        response = run_agent()

        display_result(response)

    except Exception as error:

        print("\n❌ AGENT ERROR")
        print("-" * 60)
        print(error)

        print("\nPossible causes:")
        print("1. OPENAI_API_KEY is missing.")
        print("2. The API account has no available credits.")
        print("3. The API request hit a rate limit.")
        print("4. There is a temporary API/network problem.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()