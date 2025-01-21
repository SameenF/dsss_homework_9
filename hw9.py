import logging
import re
import torch
import os
from transformers import pipeline
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Initialize the model
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
pipe = pipeline(
    "text-generation",
    model="./TinyLlama",
    tokenizer="./TinyLlama",
    torch_dtype=torch.float16,  # Use float16 precision
    device=device,
)

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your AI assistant. How can I help you today?")
    logging.info("Responded to /start")

# Stop command handler
async def stop(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Goodbye! Shutting down the bot...")
    logging.info("Bot is shutting down...")
    os._exit(0)

# Message handler
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logging.info(f"Received user message: {user_message}")

    # Check for specific input like "Hello World" or "Hello AI Assistant"
    if user_message.lower() in ["hello world", "hello ai assistant"]:
        response = "Hi there! I am here to assist you. Ask me anything!"
        await update.message.reply_text(response)
        logging.info(f"Special greeting sent: {response}")
        return

    # Use the model to generate a reply for other inputs
    messages = [
        {"role": "system", "content": "You are an AI chatbot!"},
        {"role": "user", "content": user_message},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)

    # Extract only the assistant's response
    full_reply = outputs[0]["generated_text"]

    # Remove <system>, <user>, <assistant>, and any unwanted tags
    cleaned_reply = re.sub(r"<.*?>", "", full_reply).strip()

    # Ensure no remnants of the system/user messages
    if "You are an AI chatbot!" in cleaned_reply:
        cleaned_reply = cleaned_reply.replace("You are an AI chatbot!", "").strip()
    if user_message in cleaned_reply:
        cleaned_reply = cleaned_reply.replace(user_message, "").strip()

    # Send the cleaned reply back to the user
    await update.message.reply_text(cleaned_reply)
    logging.info(f"Reply sent: {cleaned_reply}")

# Main function to start the bot
def main():
    api_token = "7572346119:AAFgDNoU7mL8LoKhjzmfT29IAaNWVel0m50"

    application = ApplicationBuilder().token(api_token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logging.info("Bot is running!")
    application.run_polling()

if __name__ == "__main__":
    main()
