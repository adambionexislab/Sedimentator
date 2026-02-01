from openai import OpenAI

client = OpenAI()


def generate_llm_report(summary, days=30):
    """
    Generates a professional operational report based on aggregated statistics.
    """

    prompt = f"""
You are a wastewater treatment process expert.

Write a concise operational report based on the last {days} days of data.

FACTS (do not invent numbers and list them in a small table):
- Number of predictions: {summary['rows']}
- Average COD: {summary['avg_COD']} ppm
- Average SVI: {summary['avg_SVI']}
- Average SS: {summary['avg_SS']} g/L
- Average Flow: {summary['avg_FLOW']} m3/h
- Average Flocculant Dose: {summary['avg_DOSE']} L/h
- Average Sludge Height: {summary['avg_SLUDGE']} cm
- % of time sludge > 85 cm: {summary['pct_above_85']} %
- % of time sludge > 100 cm: {summary['pct_above_100']} %

CONSTRAINTS:
- Sludge target = 85 cm
- Sludge limit = 100 cm
- Goal: minimize flocculant usage while staying below limits

STRUCTURE YOUR REPORT WITH THESE SECTIONS:
1. Executive Summary
2. Process Performance
3. Flocculant Usage & Cost Efficiency
4. Operational Risks
5. Recommendations

Tone:
- Clear
- Professional
- Operator-friendly
- No speculation
- Dont use ## and other similar symbols to separate sections
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
