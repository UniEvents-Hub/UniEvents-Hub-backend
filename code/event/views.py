from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated  # Import AllowAny permission
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from .models import Event, Ticket, Saved
from .serializers import EventSerializer, TicketSerializer,SavedSerializer
from rest_framework.response import Response
import json
from rest_framework.generics import UpdateAPIView
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework import permissions
import base64
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
import stripe 
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import os
import random

stripe.api_key = settings.STRIPE_SECRET_KEY

class IsEventCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the creator of the event
        return obj.user.id == request.user.id

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for creating events
    #authentication_classes = [SessionAuthentication]  # Use session authentication

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)

class EventRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]  # Allow access to any user

    def get(self, request):
        try:
            filter_column_value = request.query_params.get('event_id')
        except ValueError:
            return Response({'error': 'Invalid filter_column_value'}, status=400)
        
        if filter_column_value:
            queryset = Event.objects.filter(id=filter_column_value)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No filter_column_value provided'}, status=400)

class UserEventRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsEventCreator]  # Require authentication and check if the user is the event creator

    def get(self, request):
        try:
            filter_column_value = request.query_params.get('user_id')
        except ValueError:
            return Response({'error': 'Invalid filter_column_value'}, status=400)
        
        if filter_column_value:
            queryset = Event.objects.filter(user=filter_column_value)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No filter_column_value provided'}, status=400)


class EventUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsEventCreator]  # Require authentication and check if the user is the event creator
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        event_id = self.kwargs.get('pk')  # Get event ID from URL argument
        if event_id is None:
            raise NotFound('Event ID is required.')
        try:
            return Event.objects.get(pk=event_id)  # Get event object by ID
        except Event.DoesNotExist:
            raise NotFound('Event with this ID does not exist.')

    def partial_update(self, request, *args, **kwargs):
        # No changes required here, logic remains the same for patching the retrieved object
        instance = self.get_object()
        base64_image = request.data.get('banner', None)
        if base64_image and isinstance(base64_image, str):
            # Decode the base64 image data
            image_data = base64.b64decode(base64_image)

            # Create a ContentFile instance with the image data
            file_name = f"{instance.id}_event_banner.png"
            content_file = ContentFile(image_data, name=file_name)

            # Update the request data with the ContentFile instance
            request.data['banner'] = content_file
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            filter_column_value = request.query_params.get('event_type')
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'}, status=400)
        
        # Fetch all rows of the desired table
        if filter_column_value == "all":
            # Filter the queryset based on the filter column value
            queryset = Event.objects.all()
        else:
            # No filter parameter provided, return all rows
            queryset = Event.objects.filter(event_type=filter_column_value)
        
        # Serialize the queryset
        serializer = EventSerializer(queryset, many=True)
        # Return the serialized data as JSON
        return Response(serializer.data)
    
    
class TicketCreateAPIView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        # Decrease ticket_number
        event_id = request.data.get('event')
        if event_id:
            try:
                ticket = Event.objects.filter(id=event_id).order_by('total_tickets').first()
                if ticket.total_tickets_remaining-request.data.get("ticket_number")>=0:
                    ticket.total_tickets_sold  += request.data.get("ticket_number")
                    ticket.total_tickets_remaining -= request.data.get("ticket_number")
                    ticket.save()
                else:
                    return Response({"error": "No available tickets for this event"}, status=status.HTTP_400_BAD_REQUEST)
            except Ticket.DoesNotExist:
                return Response({"error": "Ticket not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Event ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        response =  super().create(request, *args, **kwargs)
        # Retrieve event details for email content
        event_data = EventSerializer(ticket).data
        ticket_created = Ticket.objects.filter(event=event_id).order_by("id").last()
        ticket_created_data =TicketSerializer(ticket_created).data
        
        response = {**response.data, **event_data, **ticket_created_data}
        # Send email to the user
        ticket_data = response
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        email = user.email
        
        #subject = 'Ticket Purchase Confirmation'
        #message = render_to_string('ticket_email.html', {'ticket_data': ticket_data})
        #from_email = 'shovon6446@gmail.com'  # Change this to your email address
        #to_email = [email]
        #send_mail(subject, message, from_email, to_email, fail_silently=True)
        
         # Generate email content
        html_content = render_to_string('ticket_email.html', {'ticket_data': ticket_data, 'user': user})
        text_content = strip_tags(html_content)
         # Generate PDF
        pdf_buffer = BytesIO()
        pdf_doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

        order = random.randint(4000,6000)
        invoice = random.randint(10500,12000)
        elements = []
        data = [
            ['Event', ticket_data['title']],
            ['Date', ticket_data['date']],
            ['Time', f"{ticket_data['start_time']} - {ticket_data['end_time']}"],
            ['Location', ticket_data['address']],
            ['Ticket Number', ticket_data['ticket_number']],
            ['Total Cost', ticket_data['total_cost']],
            ['Order ID', order],
            ['Invoice ID', invoice]
        ]
        
        # Define the column widths (adjust as needed)
        col_widths = [120, 300]  # Widths for the two columns

        table = Table(data, colWidths=col_widths)

        table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        table.setStyle(table_style)
        elements.append(table)
        # Create PDF document
        pdf_doc.build(elements)
        pdf_filename = f'ticket_{ticket_created_data["id"]}.pdf'  # Customize filename as needed
        
        #saving_path = f"../../mediafiles/{pdf_filename}"

        # Attach PDF to email
        email = EmailMessage(
            subject='Ticket Purchase Confirmation',
            body=text_content,
            from_email='shovon6446@gmail.com',
            to=[email]
        )
        email.attach(pdf_filename, pdf_buffer.getvalue(), 'application/pdf')
        email.send(fail_silently=True)
        
        
        #response = {**response.data, **event_data}
        saving_path = os.path.join(settings.MEDIA_ROOT, "tickets", pdf_filename)

        # Save the PDF file to the specified path
        with open(saving_path, 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.getvalue())

        ticket_created = Ticket.objects.get(id=ticket_created_data["id"])
        ticket_created.ticket_pdf = f"/media/tickets/{pdf_filename}"
        ticket_created.order_id  = order
        ticket_created.invoice_id = invoice
        ticket_created.save()
        response["ticket_pdf"] = f"/media/tickets/{pdf_filename}"
        response["order_id"] = order
        response["invoice_id"] = invoice
        
        return Response({"success": "Ticket purchase successful", "ticket": response}, status=status.HTTP_201_CREATED)

    
class UserTicketAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        return Ticket.objects.filter(user=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        Ticket_serializer = TicketSerializer(queryset, many=True)
        
        # Serialize each related event individually
        event_data = []
        for ticket in queryset:
            event_data.append(EventSerializer(ticket.event).data)
        
        # Combine ticket data with event details
        response_data = []
        for ticket, event in zip(Ticket_serializer.data, event_data):
            response_data.append({**ticket, 'event': event})
        
        return Response(response_data)
    
class UserTicketDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            ticket_id = kwargs['pk']  # Retrieve ticket ID from URL kwargs
            ticket = self.get_queryset().get(id=ticket_id, user=request.user)  # Ensure ticket belongs to current user
            serializer = self.get_serializer(ticket)

            # Serialize related event data
            event_data = EventSerializer(ticket.event).data

            # Combine ticket data with event details
            response_data = {**serializer.data, 'event': event_data}
            return Response(response_data)

        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    

class SavedCreateAPIView(generics.CreateAPIView):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed

class UserSavedAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Saved.objects.filter(user=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        saved_serializer = SavedSerializer(queryset, many=True)
        
        # Serialize each related event individually
        event_data = []
        for saved_item in queryset:
            event_data.append(EventSerializer(saved_item.event).data)
        
        # Combine saved data with event details
        response_data = []
        for saved, event in zip(saved_serializer.data, event_data):
            response_data.append({**saved, 'event': event})
        
        return Response(response_data)
        

class UserUnsaveAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SavedSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Saved.objects.filter(user=user_id)

    def get_object(self):
        queryset = self.get_queryset()
        data = json.loads(self.request.body)
        user_id = data.get('user')
        event_id = data.get('event')

        obj = queryset.filter(user=user_id, event=event_id).first()
        if obj:
            return obj
        else:
            raise Saved.DoesNotExist

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'success': 'Item unsaved'}, status=status.HTTP_204_NO_CONTENT)
        except Saved.DoesNotExist:
            return Response({'error': 'Saved item not found'}, status=status.HTTP_404_NOT_FOUND)
        

class CheckSavedAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Saved.objects.filter(user=user_id)

    def retrieve(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        queryset = self.get_queryset()

        # Check if the user has saved the event
        saved = queryset.filter(event=event_id).exists()

        if saved:
            return Response({'saved': True}, status=status.HTTP_200_OK)
        else:
            return Response({'saved': False}, status=status.HTTP_200_OK)
        

class CreateCheckoutSessionView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'cad',
                            'product_data': {
                                'name': 'Your product name',
                            },
                            'unit_amount': 2000,  # Amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='https://your.site.com/success',
                cancel_url='https://your.site.com/cancel',
            )
            return Response({'sessionId': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)