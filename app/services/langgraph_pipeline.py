import logging
from typing import Any, TypedDict

from app.services.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class ChatState(TypedDict):
    """State for the chat pipeline"""

    messages: list[dict[str, str]]
    user_message: str
    context: str
    response: str
    is_safe: bool
    metadata: dict[str, Any]


class LangGraphPipeline:
    """
    Simple LangGraph-inspired pipeline for parenting chat
    """

    def __init__(self):
        self.openai_client = OpenAIClient()

    async def process_chat(
        self, user_message: str, conversation_history: list[dict] = None
    ) -> dict[str, Any]:
        """
        Process chat through pipeline steps:
        1. Input moderation
        2. Context retrieval (placeholder)
        3. Response generation
        4. Output moderation
        """

        # Initialize state
        state = ChatState(
            messages=conversation_history or [],
            user_message=user_message,
            context="",
            response="",
            is_safe=True,
            metadata={},
        )

        try:
            # Step 1: Input moderation
            state = await self._moderate_input(state)
            if not state["is_safe"]:
                return self._create_safety_response(state)

            # Step 2: Add context (placeholder for now)
            state = await self._add_context(state)

            # Step 3: Generate response
            state = await self._generate_response(state)

            # Step 4: Output moderation
            state = await self._moderate_output(state)

            return {
                "response": state["response"],
                "is_safe": state["is_safe"],
                "metadata": state["metadata"],
            }

        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again.",
                "is_safe": True,
                "metadata": {"error": str(e)},
            }

    async def _moderate_input(self, state: ChatState) -> ChatState:
        """Moderate user input"""
        try:
            moderation = await self.openai_client.moderate_content(
                state["user_message"]
            )
            state["is_safe"] = not moderation.flagged

            if moderation.flagged:
                state["metadata"]["moderation_reason"] = "Input flagged by moderation"

        except Exception as e:
            logger.warning(f"Input moderation failed: {e}")
            # Fail open for now
            state["is_safe"] = True

        return state

    async def _add_context(self, state: ChatState) -> ChatState:
        """Add relevant context (placeholder for RAG)"""
        # TODO: Implement vector search and retrieval
        state[
            "context"
        ] = """
        You are a helpful parenting assistant. Provide supportive, evidence-based advice 
        while being empathetic and understanding. Always prioritize child safety and well-being.
        """
        return state

    async def _generate_response(self, state: ChatState) -> ChatState:
        """Generate AI response"""

        # Build conversation history
        messages = [{"role": "system", "content": state["context"]}]

        # Add conversation history
        messages.extend(state["messages"][-5:])  # Last 5 messages for context

        # Add current user message
        messages.append({"role": "user", "content": state["user_message"]})

        # Generate response
        response = await self.openai_client.chat_completion(
            messages=messages, model="gpt-4o-mini", max_tokens=500, temperature=0.7
        )

        state["response"] = response.choices[0].message.content
        state["metadata"]["model"] = "gpt-4o-mini"
        state["metadata"]["usage"] = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

        return state

    async def _moderate_output(self, state: ChatState) -> ChatState:
        """Moderate AI output"""
        try:
            moderation = await self.openai_client.moderate_content(state["response"])
            if moderation.flagged:
                state["is_safe"] = False
                state["response"] = (
                    "I apologize, but I need to rephrase my response. Let me try a different approach to help you."
                )

        except Exception as e:
            logger.warning(f"Output moderation failed: {e}")

        return state

    def _create_safety_response(self, state: ChatState) -> dict[str, Any]:
        """Create response for unsafe content"""
        return {
            "response": "I understand you're looking for parenting advice, but I need you to rephrase your question in a way that's appropriate for our platform.",
            "is_safe": False,
            "metadata": state["metadata"],
        }
