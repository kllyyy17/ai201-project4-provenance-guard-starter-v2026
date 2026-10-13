"""
What your test runs. <- UNIT 8, MILESTONE 3

One scenario per criterion in criteria.md:

    1. Human writing is rarely accused      10 human-written pieces
    2. AI and human score apart             5 AI + 5 human (mean gap >= 0.25)
    3. All three labels reachable           5 AI + 5 human + 5 borderline
    4. Appeal recorded, decision kept       NOT here — see appeal_check.py
    5. Empty text refused                   bodies: "" and "   "

The text sets are fixed. The same pieces are used in every trial and every run,
so a change in results comes from the service, not from the inputs.
validate() refuses to run if any placeholder text remains.

Scenario names must differ in their first 12 characters: run_eval.py builds the
creator_id from them, and the rate limiter (5/minute per creator_id) would
otherwise treat two scenarios as one caller.
"""

# ── Human-written ────────────────────────────────────────────────────────────
# Ten pieces written by the author, in the author's own voice. Five are plain
# and neutral (messages, a routine, advice, a statement of interest), the kind
# of writing where the model signal is weakest. Five are casual, humorous,
# first-person anecdotes. They alternate, so the first five, which also serve
# as the human group in criteria 2 and 3, contain both kinds (3 plain, 2
# anecdotal).
HUMAN = [
    # 1. plain: work message
    "Hi, I've updated the driver for the RAFT tool, and I'm checking if everything "
    "works correctly now. I'm also working on the vulnerability findings for SMID "
    "and DC Temp. After I finish those, I'll continue working on the MDH migration "
    "for DC Temp. Please let me know if there is another task I should focus on "
    "first.",

    # 2. anecdotal: work bug
    "Spent 2 hours fixing a bug today just to realize I broke it myself yesterday. "
    "Nobody tells you software engineering is basically leaving problems for your "
    "future self and then getting mad when you meet him. Anyway, it's fixed now and"
    " I'm taking full credit for the solution.",

    # 3. plain: daily routine
    "My weekdays are usually pretty similar. I wake up, get ready, and go to work. "
    "After work, I sometimes go to the gym, or I just stay home and study. I try to"
    " eat enough protein and drink enough water every day. At night, I usually "
    "spend some time on my computer before going to sleep. My life is not very "
    "exciting during the week, but I like having a routine.",

    # 4. anecdotal: gym
    "Went to the gym after work even though I was tired. Got there and the one "
    "machine I needed was occupied by a guy who looked like he was negotiating a "
    "mortgage between sets. I waited 10 minutes and he was still on his phone. "
    "Anyway, I did a different exercise and went home feeling like I survived a "
    "very stupid side quest.",

    # 5. plain: cancelling plans
    "Hey, sorry, I don't think I can make it today. I have a few things I need to "
    "take care of, and I don't think I'll have enough time. Can we meet another day"
    " instead? Sorry for telling you this so late.",

    # 6. anecdotal: Costco
    "Went to Costco for milk. Came back with yogurt, salmon, chicken, a giant bag "
    "of broccoli, and enough protein snacks to survive a minor emergency. The "
    "cashier asked if I found everything okay and I said yes like I hadn't just "
    "spent 20 minutes comparing two kinds of yogurt. I need a shopping list and "
    "apparently also someone to supervise me.",

    # 7. plain: advice to a new student
    "My advice is to take advantage of the opportunities you have in college. Don't"
    " only focus on classes and grades. Try new things, meet different people, and "
    "find out what you enjoy. You don't need to know exactly what you want to do "
    "with your life right away. I think the important thing is to keep learning and"
    " be open to new opportunities. You will learn more about yourself as you get "
    "more experience.",

    # 8. anecdotal: sleep
    "I can be falling asleep at my desk at 3 PM, but the second I get into bed at "
    "night my brain suddenly remembers an awkward conversation from 2019. Now I'm "
    "lying there thinking about what I should've said to a cashier six years ago. "
    "Very cool. Apparently my brain has unlimited storage but uses it exclusively "
    "for useless information.",

    # 9. plain: why my major
    "I've been interested in computers since I was young. At first, I mostly used "
    "them to play games, but later I started learning how to code. I realized that "
    "computers can do many things besides playing games, and I became interested in"
    " how software works. I like computer science because I can solve problems and "
    "create something useful. There are still many things I need to learn, and "
    "that's one reason I want to keep improving.",

    # 10. anecdotal: job postings
    "Sometimes I look at job postings asking for 5 years of experience with a "
    "technology released 2 years ago and wonder if I'm supposed to invent a time "
    "machine before applying. Every position wants cloud, distributed systems, AI, "
    "17 programming languages, and apparently the ability to communicate with "
    "ancient civilizations. I'm just trying to become a better engineer one project"
    " at a time, man.",
]

# ── AI-generated ─────────────────────────────────────────────────────────────
# Five pieces generated by an AI tool, unedited. Topics: AI, time management,
# climate change, remote work, exercise. Used in criteria 2 and 3.
AI = [
    "Artificial intelligence is transforming the way we live and work. By "
    "automating routine tasks, it allows people to focus on more creative and "
    "strategic endeavors. However, it is important to consider the ethical "
    "implications of these technologies. Ultimately, a balanced approach will "
    "ensure that the benefits of AI are shared by all.",

    "Time management is a crucial skill for students in today's fast-paced "
    "world. By setting clear goals, prioritizing tasks, and minimizing "
    "distractions, students can improve their productivity. Furthermore, "
    "regular breaks help maintain focus and prevent burnout. In conclusion, "
    "effective time management leads to both academic success and personal "
    "well-being.",

    "Climate change represents one of the most significant challenges facing "
    "humanity. Rising global temperatures contribute to extreme weather events, "
    "sea level rise, and loss of biodiversity. To address this issue, "
    "governments, businesses, and individuals must work together. Sustainable "
    "practices and renewable energy are essential steps toward a healthier "
    "planet.",

    "Remote work has become increasingly popular in recent years. It offers "
    "employees greater flexibility, reduces commuting time, and can improve "
    "work-life balance. At the same time, it presents challenges such as "
    "isolation and difficulty collaborating. Organizations that invest in clear "
    "communication and supportive culture are best positioned to succeed.",

    "Regular exercise provides numerous benefits for both physical and mental "
    "health. It strengthens the cardiovascular system, improves mood, and "
    "enhances sleep quality. Moreover, even moderate activity, such as walking "
    "for thirty minutes a day, can make a meaningful difference. Consistency is "
    "the key to long-term results.",
]

# ── Borderline, chosen by ORIGIN (criteria.md #3) ────────────────────────────
# Five pieces of mixed origin, grouped by how they were made, not by how they
# score. None were tuned to hit a score.
# 3 AI drafts edited by hand: reworded, with personal details added.
# 2 mixed pieces: one half human-written, the other half AI-generated, joined
#   into a single paragraph (one human-first, one AI-first).
BORDERLINE = [
    # edited AI 1: learning a language
    "Learning a new language takes time and a lot of practice. When I first moved "
    "to the United States, I had to learn many new things, including how to "
    "communicate with people in English. Sometimes I didn't understand what people "
    "were saying, especially when they spoke too fast. I think making mistakes is "
    "normal because you cannot improve if you never try. The more you practice, the "
    "more comfortable you become.",

    # edited AI 2: social media
    "Social media makes it easier for people to communicate and share information "
    "with each other. We can learn about things happening around the world without "
    "leaving our homes. However, not everything people post online is true, and "
    "sometimes I find myself spending more time scrolling than I planned. I think "
    "social media is useful, but people should be careful about what they believe "
    "and how much time they spend on it.",

    # edited AI 3: healthy diet
    "Eating healthy is important, but it doesn't mean you have to change everything "
    "about your diet at once. I try to eat fruits and vegetables every day and get "
    "enough protein because I'm also trying to build muscle. Sometimes it is hard "
    "to follow the same routine, especially when I'm busy with work. I think making "
    "small changes and staying consistent is better than trying to change "
    "everything in a few days.",

    # mixed 1: human first half, AI second half
    "I sat down after work to solve two LeetCode problems before bed, but I kept "
    "getting distracted. I checked one notification and somehow ended up watching "
    "videos for 20 minutes. By the time I started studying again, I was already "
    "tired and wanted to sleep. Experts suggest that breaking work into shorter "
    "intervals and removing digital distractions can substantially improve "
    "concentration. Establishing a consistent routine further reinforces these "
    "habits over time.",

    # mixed 2: AI first half, human second half
    "Public transportation plays a vital role in reducing congestion and lowering "
    "emissions in urban areas. Investing in reliable systems benefits communities "
    "of all sizes. I remember waiting for a bus and checking the time every few "
    "minutes because I didn't want to be late. There were other people waiting "
    "too, and everyone kept looking down the road to see if the bus was coming. "
    "Taking the bus can be convenient, but waiting without knowing when it will "
    "arrive is frustrating.",
]

SCENARIOS = [
    {
        "name": "c1 own writing",
        "criterion": 1,
        "texts": HUMAN,                     # all 10
    },
    {
        "name": "c2 score spread",
        "criterion": 2,
        "texts": AI + HUMAN[:5],            # first 5 = AI, last 5 = human
    },
    {
        "name": "c3 label cover",
        "criterion": 3,
        "texts": AI + HUMAN[:5] + BORDERLINE,   # 15 pieces
    },
    {
        "name": "c5 empty text",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_empty"},
            {"text": "   ", "creator_id": "eval_spaces"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
