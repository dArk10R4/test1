import os
import logging

from fastapi.responses import JSONResponse
from bot import WhatsApp
from environment import get_env
# from flask import Flask, request, make_response
from fastapi import FastAPI, HTTPException, Response, Query, Request
from pydantic import BaseModel
from flow_handler import FlowHandler
import json
from environment import get_env
# Initialize Flask App
# app = Flask(__name__)
app = FastAPI()
# Load .env file
messenger = WhatsApp(
    os.getenv("TOKEN"), 
    phone_number_id=os.getenv("PHONE_NUMBER_ID")
    )
VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

flow_handler = FlowHandler(settings = json.load(open(get_env("SETTINGS_FILE_PATH"), "r", encoding="utf-8"))
)
@app.get("/")
async def verify_token(hub_verify_token: str = Query(None, alias="hub.verify_token"), hub_challenge: str = Query(None, alias="hub.challenge"), hub_mode: str = Query(None, alias="hub.mode")):
    print(hub_verify_token)
    print(VERIFY_TOKEN)
    if hub_verify_token == VERIFY_TOKEN and hub_mode == "subscribe":
        print("Verified webhook")
        logging.info("Verified webhook")
        return Response(content=hub_challenge, media_type="text/plain")
    else:
        logging.error("Webhook Verification failed")
        raise HTTPException(status_code=400, detail="Invalid verification token")




@app.post("/")
async def hook(request: Request = None):
    if request is None:
        print("Request is None")
        return "OK"
    data = await request.json()
    # data = json.loads(raw_json)
    # Handle Webhook Subscriptions
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.is_message(data)
        if new_message:
            mobile = messenger.get_mobile(data) 
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)
                flow_handler.handle_request(data)


            # elif message_type == "interactive":
            #     message_response = messenger.get_interactive_response(data)
            #     interactive_type = message_response.get("type")
            #     message_id = message_response[interactive_type]["id"]
            #     message_text = message_response[interactive_type]["title"]
            #     logging.info(f"Interactive Message; {message_id}: {message_text}")

            # elif message_type == "location":
            #     message_location = messenger.get_location(data)
            #     message_latitude = message_location["latitude"]
            #     message_longitude = message_location["longitude"]
            #     logging.info("Location: %s, %s", message_latitude, message_longitude)

            # elif message_type == "image":
            #     image = messenger.get_image(data)
            #     image_id, mime_type = image["id"], image["mime_type"]
            #     image_url = messenger.query_media_url(image_id)
            #     image_filename = messenger.download_media(image_url, mime_type)
            #     logging.info(f"{mobile} sent image {image_filename}")

            # elif message_type == "video":
            #     video = messenger.get_video(data)
            #     video_id, mime_type = video["id"], video["mime_type"]
            #     video_url = messenger.query_media_url(video_id)
            #     video_filename = messenger.download_media(video_url, mime_type)
            #     logging.info(f"{mobile} sent video {video_filename}")

            # elif message_type == "audio":
            #     audio = messenger.get_audio(data)
            #     audio_id, mime_type = audio["id"], audio["mime_type"]
            #     audio_url = messenger.query_media_url(audio_id)
            #     audio_filename = messenger.download_media(audio_url, mime_type)
            #     logging.info(f"{mobile} sent audio {audio_filename}")

            # elif message_type == "document":
            #     file = messenger.get_document(data)
            #     file_id, mime_type = file["id"], file["mime_type"]
            #     file_url = messenger.query_media_url(file_id)
            #     file_filename = messenger.download_media(file_url, mime_type)
            #     logging.info(f"{mobile} sent file {file_filename}")
            # else:
            #     logging.info(f"{mobile} sent {message_type} ")
            #     logging.info(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                logging.info(f"Message : {delivery}")
            else:
                logging.info("No new message")
    return JSONResponse(content={"message": "OK"}, status_code=200)

# if __name__ == "__main__":
#     app.run(port=5000, debug=False)