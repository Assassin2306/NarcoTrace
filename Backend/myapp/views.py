import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import RobertaTokenizer, TFRobertaForSequenceClassification
import torch
import tensorflow as tf
from myapp.models import FlaggedMessage
import telebot  # For Telegram bot interaction
import requests  # For making HTTP requests to Django
import django  # To set up Django environment
import os  # For setting environment variables
from datetime import datetime  # For handling timestamps
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Model-related imports
import torch  # For PyTorch tensors and model inference
import tensorflow as tf  # For TensorFlow tensors
from transformers import RobertaTokenizer, TFRobertaForSequenceClassification  # Hugging Face model and tokenizer
from .serializers import FlaggedMessageSerializer

# Setup logging
logger = logging.getLogger(__name__)

# Load tokenizer and model
model_path = "D:\Roberta"
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = TFRobertaForSequenceClassification.from_pretrained(model_path)
  #change start


def predict_message(message_text):
    try:
        # Add logging for debugging
        logger.info(f"Processing message: {message_text[:100]}...")  # Log first 100 chars

        # Preprocess the input message
        inputs = tokenizer(
            message_text, 
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512  # Add max length to prevent too long sequences
        )
        
        logger.debug(f"Tokenized input shape: {inputs['input_ids'].shape}")
        
        # Convert PyTorch tensors to TensorFlow tensors
        inputs_tf = {
            "input_ids": tf.convert_to_tensor(inputs["input_ids"].numpy()),
            "attention_mask": tf.convert_to_tensor(inputs["attention_mask"].numpy())
        }
        
        # Get the model output
        outputs = model(**inputs_tf)
        
        # Process the outputs and return if drug-related
        logits = outputs.logits
        predicted_class = tf.argmax(logits, axis=-1).numpy()[0]  # Get first element
        probability = tf.nn.softmax(logits, axis=-1).numpy()[0]  # Get probabilities
        
        logger.info(f"Prediction result: class={predicted_class}, probability={probability}")
        
        return bool(predicted_class == 1)  # Ensure boolean return
        
    except Exception as e:
        logger.error(f"Error in predict_message: {str(e)}")
        raise Exception(f"Model prediction failed: {str(e)}")


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip









@csrf_exempt
def flagged_message(request):
    try:
        if request.method == 'GET':
            # Get all messages, including flagged status
            messages = FlaggedMessage.objects.all().order_by('-timestamp')
            serializer = FlaggedMessageSerializer(messages, many=True)
            data = serializer.data
            
            # Debug logging
            logger.info(f"Sending {len(data)} messages")
            for msg in data[:5]:  # Log first 5 messages
                logger.info(f"Message {msg['id']}: flagged={msg['flagged']}")
            
            response = JsonResponse(data, safe=False)
            return response
            
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                logger.info(f"Processed JSON data: {data}")

                # Create message object with pending status
                message = FlaggedMessage.objects.create(
                    message=data['message'],
                    user_id=str(data.get('user_id', 'unknown')),
                    chat_id=str(data.get('chat_id', 'unknown')),
                    processing_status='pending'
                )

                try:
                    # Process message
                    is_flagged = predict_message(data['message'])
                    
                    # Update message with results
                    message.flagged = is_flagged
                    message.processing_status = 'processed'
                    message.save()

                    # Simplified response
                    response_data = {
                        'status': 'flagged' if is_flagged else 'not flagged'
                    }
                    return JsonResponse(response_data)

                except Exception as e:
                    # Update message with error status only
                    message.processing_status = 'error'
                    message.save()
                    
                    logger.error(f"Processing error: {str(e)}")
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Processing failed: {str(e)}'
                    }, status=500)

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'Invalid JSON format: {str(e)}'
                }, status=400)

        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Method {request.method} not allowed'
            }, status=405)

    except Exception as e:
        logger.error(f"Unhandled error in flagged_message view: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }, status=500)

from django.http import JsonResponse
from .models import FlaggedMessage
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET"])
def get_flagged_messages(request):
    try:
        messages = FlaggedMessage.objects.filter(flagged=True).values()
        response = JsonResponse(list(messages), safe=False)
        return response
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        return JsonResponse(
            {'error': 'Failed to fetch messages'}, 
            status=500
        )

def flagged_message_view(request):
    return JsonResponse({"message": "Welcome to Flagged Messages Page!"})

def status_check(request):
    """
    Simple endpoint to check if the API is running
    """
    try:
        # You can add additional checks here (e.g., database connection)
        return JsonResponse({
            'status': 'ok',
            'message': 'API is running',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def get_all_messages(request):
    """New view to get all messages, including non-flagged ones"""
    try:
        messages = FlaggedMessage.objects.all().order_by('-timestamp').values(
            'id', 'message', 'user_id', 'chat_id', 'timestamp', 'flagged'
        )
        logger.info(f"Fetched {len(messages)} messages")
        return JsonResponse(list(messages), safe=False)
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def batch_delete_messages(request):
    """
    Batch delete messages by IDs.
    
    Accepts a DELETE request with a JSON body containing a list of message_ids.
    Example: { "message_ids": [1, 2, 3] }
    
    Returns:
    - 200 OK on successful deletion
    - 400 Bad Request if message_ids is missing or not a list
    - 404 Not Found if some message IDs don't exist (with details of what was found/not found)
    - 500 Server Error for other errors
    """
    try:
        # Only allow DELETE method
        if request.method != 'DELETE':
            logger.error(f"Received {request.method} request, only DELETE is supported")
            return JsonResponse(
                {"error": f"Method {request.method} not allowed, only DELETE is supported"}, 
                status=405
            )
            
        # Parse request data
        try:
            data = json.loads(request.body)
            logger.info(f"Batch delete request data: {data}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in request body: {str(e)}")
            return JsonResponse(
                {"error": f"Invalid JSON in request body: {str(e)}"}, 
                status=400
            )
        
        if not data or 'message_ids' not in data:
            logger.error("message_ids is required but was not provided")
            return JsonResponse(
                {"error": "message_ids is required"}, 
                status=400
            )
        
        message_ids = data['message_ids']
        logger.info(f"Received message_ids for deletion: {message_ids}")
        
        if not isinstance(message_ids, list):
            logger.error(f"message_ids must be a list, got {type(message_ids)}")
            return JsonResponse(
                {"error": "message_ids must be a list of integers"}, 
                status=400
            )
        
        if len(message_ids) == 0:
            logger.error("message_ids list cannot be empty")
            return JsonResponse(
                {"error": "message_ids list cannot be empty"}, 
                status=400
            )
        
        # Convert all IDs to integers safely
        valid_ids = []
        invalid_ids = []
        
        for id_value in message_ids:
            try:
                valid_ids.append(int(id_value))
            except (ValueError, TypeError):
                invalid_ids.append(id_value)
                logger.warning(f"Invalid ID format: {id_value}")
        
        if not valid_ids:
            logger.error("No valid IDs provided for deletion")
            return JsonResponse(
                {"error": "No valid message IDs provided", "invalid_ids": invalid_ids}, 
                status=400
            )
        
        # Find messages that exist
        found_messages = FlaggedMessage.objects.filter(id__in=valid_ids)
        found_ids = [message.id for message in found_messages]
        
        logger.info(f"Found {len(found_ids)} messages to delete out of {len(valid_ids)} requested")
        
        # Check for messages that weren't found
        not_found_ids = list(set(valid_ids) - set(found_ids))
        
        # Delete found messages
        deletion_count = found_messages.delete()[0]
        logger.info(f"Deleted {deletion_count} messages")
        
        # Prepare response
        response_data = {
            "success": True,
            "deleted_count": deletion_count,
        }
        
        # Add info about invalid and not found IDs
        if invalid_ids:
            response_data["invalid_ids"] = invalid_ids
            response_data["warning"] = f"{len(invalid_ids)} invalid ID format(s)"
        
        if not_found_ids:
            response_data["not_found_ids"] = not_found_ids
            if "warning" in response_data:
                response_data["warning"] += f" and {len(not_found_ids)} message(s) not found"
            else:
                response_data["warning"] = f"{len(not_found_ids)} message(s) not found"
            
            # If nothing was deleted, return 404
            if deletion_count == 0:
                return JsonResponse(response_data, status=404)
        
        # Return success response
        return JsonResponse(response_data, status=200)
        
    except Exception as e:
        logger.error(f"Error in batch delete: {str(e)}", exc_info=True)
        return JsonResponse(
            {"error": f"Server error: {str(e)}"}, 
            status=500
        )