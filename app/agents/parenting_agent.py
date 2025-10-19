import logging

from app.schemas.message_schema import MessageResponse, MessageUsage
from app.services.langgraph_pipeline import LangGraphPipeline
from app.services.openai_client import OpenAIClient
from app.services.retrieval import RetrievalService

logger = logging.getLogger(__name__)


class ParentingAgent:
    """
    Core RAG pipeline agent for parenting advice
    Combines retrieval, reasoning, and response generation
    """

    def __init__(self):
        self.client = OpenAIClient()
        self.retrieval = RetrievalService()
        self.pipeline = LangGraphPipeline()

        self.system_prompt = """
        You are a knowledgeable, empathetic parenting advisor with expertise in:
        - Child development (0-18 years)
        - Positive parenting strategies
        - Behavioral guidance
        - Educational support
        - Family dynamics
        
        Guidelines:
        1. Always prioritize child safety and well-being
        2. Provide evidence-based advice when possible
        3. Be empathetic and non-judgmental
        4. Suggest professional help when appropriate
        5. Acknowledge when you don't know something
        6. Use retrieved context to inform your responses
        
        Format responses as helpful, actionable advice.
        """

    async def generate_response(
        self,
        user_message: str,
        conversation_id: int | None = None,
        user_id: int | None = None,
    ) -> MessageResponse:
        """
        Generate parenting advice using RAG pipeline
        """
        try:
            # Step 1: Retrieve relevant context
            retrieved_docs = await self.retrieval.search_relevant_content(
                query=user_message, top_k=5
            )

            # Step 2: Process through LangGraph pipeline
            pipeline_result = await self.pipeline.process_parenting_query(
                user_message=user_message,
                retrieved_context=retrieved_docs,
                conversation_history=await self._get_conversation_history(
                    conversation_id
                ),
            )

            # Step 3: Generate final response
            context_text = self._format_retrieved_context(retrieved_docs)

            messages = [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": f"""
                User question: {user_message}

                Relevant context from parenting resources:
                {context_text}
                Please provide helpful parenting advice based on this context and your expertise.
                """,
                },
            ]

            response = await self.client.chat_completion(
                messages=messages, model="gpt-4", max_tokens=800, temperature=0.7
            )

            # Format response
            ai_message = response.choices[0].message.content

            return MessageResponse(
                content=ai_message,
                role="assistant",
                conversation_id=conversation_id,
                user_id=user_id,
                model="gpt-4",
                usage=MessageUsage(
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                ),
                retrieved_sources=[
                    doc.get("source", "Unknown") for doc in retrieved_docs
                ],
            )

        except Exception as e:
            logger.error(f"Parenting agent error: {str(e)}")
            return MessageResponse(
                content="I apologize, but I'm having trouble processing your request right now. Please try again or contact support if the issue persists.",
                role="assistant",
                conversation_id=conversation_id,
                user_id=user_id,
                model="fallback",
                usage=MessageUsage(input_tokens=0, output_tokens=0, total_tokens=0),
            )

    async def _get_conversation_history(
        self, conversation_id: int | None
    ) -> list[dict]:
        """Retrieve conversation history for context"""
        if not conversation_id:
            return []

        # TODO: Implement database retrieval
        return []

    def _format_retrieved_context(self, docs: list[dict]) -> str:
        """Format retrieved documents for prompt context"""
        if not docs:
            return "No specific context found in parenting resources."

        formatted = []
        for i, doc in enumerate(docs, 1):
            content = doc.get("content", "")[:500]  # Limit length
            source = doc.get("source", "Unknown source")
            formatted.append(f"{i}. {content}... (Source: {source})")

        return "\n".join(formatted)
