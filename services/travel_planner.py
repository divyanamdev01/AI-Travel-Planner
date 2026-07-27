from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_trip_plan(location):

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash"
        )

        # Tourist Places
        place_prompt = ChatPromptTemplate.from_template(
            "List the top 6 tourist places in {location}. "
            "Give one place per line."
        )

        place_chain = place_prompt | llm | StrOutputParser()

        # Hotels
        hotel_prompt = ChatPromptTemplate.from_template(
            "Suggest 3 good hotels in {location}."
        )

        hotel_chain = hotel_prompt | llm | StrOutputParser()

        # Itinerary
        itinerary_prompt = ChatPromptTemplate.from_template(
            "Create a detailed 3-day itinerary for visiting these places: {places}"
        )

        itinerary_chain = itinerary_prompt | llm | StrOutputParser()

        # Budget
        budget_prompt = ChatPromptTemplate.from_template(
            "Estimate a budget for a 3-day trip based on this itinerary: {itinerary}"
        )

        budget_chain = budget_prompt | llm | StrOutputParser()

        # Travel Tips
        tips_prompt = ChatPromptTemplate.from_template(
            "Give useful travel tips for visiting {location}"
        )

        tips_chain = tips_prompt | llm | StrOutputParser()

        # Invoke
        places = place_chain.invoke({
            "location": location
        })

        hotels = hotel_chain.invoke({
            "location": location
        })

        itinerary = itinerary_chain.invoke({
            "places": places
        })

        budget = budget_chain.invoke({
            "itinerary": itinerary
        })

        tips = tips_chain.invoke({
            "location": location
        })

        return {
            "places": places,
            "hotels": hotels,
            "itinerary": itinerary,
            "budget": budget,
            "tips": tips
        }

    except Exception as e:

        error_message = str(e).lower()

        if (
            "resource_exhausted" in error_message
            or "quota" in error_message
            or "429" in error_message
            or "rate limit" in error_message
        ):
            return {
                "error": "TOKEN_LIMIT"
            }

        return {
            "error": str(e)
        }