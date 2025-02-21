# Move all prompts here from previous files
URL_ANALYSIS_PROMPT = """Analyze this URL with extreme precision and complete objectivity to determine if it is phishing or legitimate:

URL to analyze: {url}

You MUST return a valid JSON object with this EXACT structure:
{{
    "is_phishing": boolean,
    "indicators": {{
        "suspicious": [
            "string1",
            "string2"
        ],
        "legitimate": [
            "string1",
            "string2"
        ]
    }},
    "explanation": "string"
}}

CRITICAL: Your response must be ONLY the JSON object above, with no additional text or formatting.

ANALYSIS REQUIREMENTS:
1. Analyze ONLY verifiable technical elements:
   - Domain analysis:
     * TLD legitimacy and category
     * Domain age, registration details, and expiry
     * DNS records and nameservers
     * Domain reputation across security databases
     * Subdomain structure and patterns
   
   - SSL/TLS verification:
     * Certificate validity and expiration
     * Certificate authority legitimacy
     * SSL/TLS version and security level
     * Certificate transparency logs
   
   - URL structure analysis:
     * Path and query parameter patterns
     * URL encoding anomalies
     * Character set and encoding schemes
     * Presence of suspicious keywords
     * Length and complexity metrics
   
   - Redirect chain analysis:
     * Number and types of redirects
     * Geographic location of redirects
     * Protocol changes in redirect chain
     * Final destination analysis
   
   - Technical infrastructure:
     * IP address reputation
     * Hosting provider legitimacy
     * Geographic location consistency
     * Associated infrastructure patterns

2. Maintain strict objectivity:
   - Analyze all technical elements equally
   - Document all findings without bias
   - Base decision solely on technical evidence
   - No assumptions or preconceptions

3. Make a binary decision:
   - Evaluate evidence objectively
   - Decision must be based on concrete findings
   - Document exact technical reasons for decision"""

FACT_IDENTIFICATION_PROMPT = """You are a highly selective fact identification system focused solely on phishing detection. Your goal is to minimize costs by identifying ONLY facts that are critical for determining if a message is phishing or legitimate.

BUSINESS CONTEXT:
- Each fact requires an expensive Perplexity API call for verifying the veracity or falsity of the fact.
- Only identify facts that directly indicate phishing/legitimacy
- Ignore facts unrelated to phishing detection
- Be extremely selective to minimize API costs

Return in this JSON format:
{
    "has_facts": boolean,
    "facts": [string] or null  // ONLY the 1-2 most critical factual claims
}

SELECTION CRITERIA:
- Focus on claims that are central to the message's credibility
- Ignore personal statements, opinions, or casual mentions
- Prioritize claims about institutions, systems, or official entities
- Only select facts where verification would significantly impact trust assessment

Text to analyze: {user_input}""" 

FACT_CHECK_PROMPT = """Original message: {user_input}

Facts identified for verification:
{facts}

Return in this JSON format:
{
    "verified_facts": [
        {
            "claim": string,
            "is_true": boolean,
            "explanation": string,
            "sources": {
                "urls": ["single_most_authoritative_url"],  // ONLY ONE most reliable source URL per fact
                "references": []  // Keep empty, we only need the URL
            }
        }
    ]
}

CRITICAL REQUIREMENTS:
1. Return ONLY ONE source URL per fact - choose the most authoritative source
2. Prioritize official documentation and company websites (e.g., microsoft.com, google.com)
3. Ensure URL is direct and accessible (no login required)
4. Do not include any reference numbers or citations
5. If a fact cannot be verified with a reliable source, exclude it from the results

RESPONSE MUST:
- Include exactly one URL per fact
- Use only official or highly trusted sources
- Never invent or hallucinate sources
- Skip facts that cannot be verified with a reliable source"""

FINAL_ANALYSIS_PROMPT = """You are {character}. You are an expert phishing analyst and your main goal is to prevent false positives. As this character, deliver a concise but powerful analysis of this message. Use the provided evidence to reason through your final decision. Don't be shy to say it if the message is clearly legitimate despite some evidence. Be direct and impactful.


Message to analyze: {user_input}


Available Evidence:
1. Message Analysis: {message_classification}
2. URL Analysis: {url_analysis}
3. Fact Verification: {fact_results}


ANALYSIS REQUIREMENTS:
1. Character Voice:
   - Stay completely in character
   - React as your character would
   - Never explain who you are
   - Keep your personality strong but brief


2. Technical Depth:
   - Hit the key technical points hard
   - Include critical verified facts in great detail with sources
   - No fluff, just the crucial findings


OUTPUT STRUCTURE:
1. Opening: Your immediate reaction, Set the tone (1 line). no need to write "Opening" or "intro" or anything like that. just get in straight.


2. Critical Findings (4-5 bullet points):
   - Most damning technical evidence from the message analysis
   - Most damning technical evidence from the URL analysis
   - Key verified facts with their detailed explanations and URL sources
   - Final reasoning considering the message context, technical and factual evidence at hand.
   
3. Verdict & Action (1 line):
   - Straight verdict (legitimate or phishing)
   - Essential security advice


CRITICAL:
- Keep it sharp and impactful
- Stay in character 100%
- Include all key technical details
- Include all factual details with sources
- Never mention internal processes or models like "optimum", "the URL model", etc.
- Maximum 3 paragraphs total
- Make every word count"""

RAG_ANALYSIS_PROMPT = """Analyze this message using the provided context for phishing detection:

Message: {text}
Similar case explanation: {explanation}
Similarity score: {similarity}%

Return a JSON object with this EXACT structure:
{{
    "is_phishing": boolean,
    "confidence": number between 0.51 and 0.95,
    "indicators": {{
        "suspicious": ["list", "of", "suspicious", "elements"],
        "legitimate": ["list", "of", "legitimate", "elements"]
    }},
    "explanation": "detailed analysis incorporating similar case insights"
}}

REQUIREMENTS:
1. Use the similar case explanation if similarity > 70%
2. Focus on patterns and indicators that match or differ from the similar case
3. Maintain objectivity in analysis
4. Provide specific, actionable indicators
5. Include confidence level based on similarity and analysis

CRITICAL: Return ONLY the JSON object with no additional text."""
