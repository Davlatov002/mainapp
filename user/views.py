from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, Transaction
from drf_yasg.utils import swagger_auto_schema
from .serialazers import ProfileSerializer, ProfilesingupSerialazer, ProfileLoginserialazer, UpdateProfileSerializer, ProfileRefeleshSerialazer,VerificationCodeserialazer ,GMProfileserialazer, UpdatePasswordSerializer, Tranzaktionserialazer, UpdateEmPsSerializer,UserTranzaktionserialazer
import time, calendar
import random
from datetime import datetime, timedelta
from django.db.models import Sum, F


# gmail######
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

globals
code_lis = {}

def send_email(subject, body, to_email):
    # Gmail pochtangiz va parolingizni kiriting
    gmail_user = 'pythonN15Django@gmail.com'
    gmail_password = 'hqmwjojhkgufgjsj'

    # Xabar tayyorlash
    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = to_email
    message['Subject'] = subject

    # Xabarning matnini qo'shish
    message.attach(MIMEText(body, 'plain'))

    # SMTP serveriga ulanish
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)

        # Xabarni yuborish
        server.sendmail(gmail_user, to_email, message.as_string())
#####

@swagger_auto_schema(method='PATCH', request_body=GMProfileserialazer, operation_description="Tiklamoqchi bo'lgan profilning ID sini kirting!")
@api_view(['PATCH'])
def send_otp(request):
    if request.method == 'PATCH':
        try:
            email = request.data.get("email")
            profile = Profile.objects.get(email=email)
        except:
            return Response({'error': -2 }, status=status.HTTP_400_BAD_REQUEST)
        six_digit_number = str(random.randint(100000, 999999))
        gmail = str(profile.email)
        send_email("Verification code",f'{  six_digit_number  }', gmail)
        code_lis[six_digit_number]=gmail
        return Response({'message': 1 },status=status.HTTP_200_OK)
    else:
        return Response({'message': -1 },status=status.HTTP_400_BAD_REQUEST)
        
@swagger_auto_schema(method='PATCH', request_body=VerificationCodeserialazer, operation_description="Tiklamoqchi bo'lgan profilning ID sini kirting!")
@api_view(['PATCH'])
def confirmation_otp(request):
    if request.method == 'PATCH':
        code = request.data.get("code")
        if code in code_lis.keys():
            del code_lis[code]
            return Response({'message': 1 }, status=status.HTTP_200_OK)
        else:
            return Response({'message': -2 },status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'message': -1 },status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='PATCH', request_body=UpdatePasswordSerializer, operation_description="Parolni o'zgartirish uchun so'rov")
@api_view(['PATCH'])
def update_password(request, email):
    try:
        profile = Profile.objects.get(email=email)
    except Profile.DoesNotExist:
        return Response({'message': -2 }, status=status.HTTP_404_NOT_FOUND)
    serializer = UpdatePasswordSerializer(data=request.data)
    if serializer.is_valid():
        new_password = serializer.validated_data['password']
        profile.password = new_password
        profile.save()
        return Response({'message': 1 }, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='PATCH', request_body=UpdateProfileSerializer, operation_description="Yangilamaoqchi bo'lgan Profilening ID sini kirting")
@api_view(['PATCH'])
def update_profile(request, pk):
    if request.method == "PATCH":
        try:
            profile = Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            return Response({'message': -1}, status=status.HTTP_404_NOT_FOUND)

        data = UpdateProfileSerializer(instance=profile, data=request.data)
        if data.is_valid():
            new_username = data.validated_data.get('username')

            if Profile.objects.filter(username=new_username).exclude(id=pk).exists():
                return Response({'message': -4}, status=status.HTTP_400_BAD_REQUEST)

            # Update profile fields
            data.save()

            # Reload the profile instance to get the updated data
            profile.refresh_from_db()

            # Serialize the updated profile for the response
            serializer = ProfileSerializer(profile)
            
            return Response({'message': 1, "profile": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': -3}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PATCH', request_body=UpdateEmPsSerializer, operation_description="Yangilamaoqchi bo'lgan Profilening ID sini kirting")
@api_view(['PATCH'])
def update_email_password(request, pk):
    if request.method == "PATCH":
        try:
            profile = Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            return Response({'message': -1}, status=status.HTTP_404_NOT_FOUND)

        data = UpdateEmPsSerializer(instance=profile, data=request.data)
        if data.is_valid():
            new_email = data.validated_data.get('email')

            if Profile.objects.filter(email=new_email).exclude(id=pk).exists():
                return Response({'message': -4}, status=status.HTTP_400_BAD_REQUEST)

            # Update profile fields
            data.save()

            # Reload the profile instance to get the updated data
            profile.refresh_from_db()

            # Serialize the updated profile for the response
            serializer = ProfileSerializer(profile)
            
            return Response({'message': 1, "profile": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': -3}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PATCH', operation_description="O'chirmoqchi bo'lgan Profileni ID sini kirting")
@api_view(['PATCH'])
def archive_account(request, pk):
    if request.method == 'PATCH':
        profile = Profile.objects.get(id=pk)
        is_data = int(time.time())
        profile.is_archived = is_data
        profile.save()
        return Response({'message': 1}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PATCH', operation_description="O'chirmoqchi bo'lgan Profileni ID sini kirting")
@api_view(['PATCH'])
def verify_email(request, pk):
    if request.method == 'PATCH':
        try:
            profile = Profile.objects.get(id=pk)
        except:
            return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
        is_data = int(time.time())
        profile.is_verified = is_data
        profile.save()
        return Response({'message': 1}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='POST', request_body=ProfilesingupSerialazer, operation_description="Malumotlarni kirting")
@api_view(['POST'])
def signup(request):
    if request.method == "POST":
        profiles = Profile.objects.all()
        usernames = [profile.username for profile in profiles]
        username = request.data.get('username')
        email = request.data.get('email')
        mac_adres = request.data.get('mac_address', None) 
        adress = [profile.mac_address for profile in profiles if profile.mac_address is not None and profile.mac_address != "null" and profile.mac_address != ""]
        gm = [profile.email for profile in profiles]
        serializer = ProfileSerializer(data=request.data)
        if username in usernames:
            return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
        elif email in gm:
            return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
        elif mac_adres in adress:
            return Response({'message': -3}, status=status.HTTP_400_BAD_REQUEST)
        elif serializer.is_valid():
            serializer.save()
            return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_profile(request):
    if request.method == 'GET':
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_profile_id(request, pk):
    if request.method == 'GET':
        profile = Profile.objects.get(id=pk)
        serializer = ProfileSerializer(profile)
        return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_profile_username(request, username):
    if request.method == 'GET':
        profile = Profile.objects.get(username=username)
        serializer = ProfileSerializer(profile)
        return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='POST', request_body=ProfileLoginserialazer, operation_description="Malumotlarni kirting")
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            profile = Profile.objects.get(username=username)
        except:
            return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
        if profile:
            if profile.password == password:
                profile_serializer = ProfileSerializer(profile)
                return Response({'message': 1, "profile":profile_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='DELETE', operation_description="O'chirmoqchi bo'lgan Profileni ID sini kirting")
@api_view(['DELETE'])
def delete_profile(request, pk):
    if request.method == 'DELETE':
        try:
            praduct = Profile.objects.get(id=pk)
        except:
            return Response({'message': -2 },status=status.HTTP_400_BAD_REQUEST)
        praduct.delete()
        return Response({'message':1},status=status.HTTP_200_OK)
    else:
        return Response({'message': -1 },status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='PATCH', request_body=ProfileRefeleshSerialazer, operation_description="Referal_link")
@api_view(['PATCH'])
def activate_referral_link(request, pk):
    if request.method == 'PATCH':
        referal = request.data.get('referal_link')
        try:
            frend = Profile.objects.get(referal_link=referal)
        except:
            return Response({'message': -2}, status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=pk)
        profile.balance_usdt += 0.1
        profile.balance_netbo += 0.2
        pr_username = str(profile.id)
        profile.save()
        taim = int(time.time())
        data = {"profile_id":pr_username, "balance_usdt":0.1,'balance_netbo':0.2,"created_at":taim}
        tran = Tranzaktionserialazer(data=data)
        if tran.is_valid():
            tran.save()
        frend.number_people += 1
        frend.balance_usdt += 0.05
        frend.balance_netbo += 0.1
        fr_username = str(frend.id)
        data = {"profile_id":fr_username, "balance_usdt":0.05,'balance_netbo':0.1,"created_at":taim}
        frend.save()
        tran = Tranzaktionserialazer(data=data)
        if tran.is_valid():
            tran.save()
        return Response({'message': 1}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PATCH', operation_description="Ball berladigan profile ID sini kirting")
@api_view(['PATCH'])
def ad_reward(request, pk):
    if request.method == 'PATCH':
        try:
            profile = Profile.objects.get(id=pk)
        except:
            return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)  
        taim2 = profile.last_mining
        taim1 = int(time.time())
        if taim2 + 14400 <= taim1 :
            if profile.number_people < 50: 
                nom = 5 + (0.1 * profile.number_people) 
                profile.balance_netbo += nom
                profile.save()
                username_id = str(profile.id)
                data = {"profile_id":username_id, 'balance_netbo':nom, "created_at":taim1}
            elif profile.number_people < 100: 
                nom = 5 + (0.2 * profile.number_people) 
                profile.balance_netbo += nom
                profile.save()
                username_id = str(profile.id)
                data = {"profile_id":username_id, 'balance_netbo':nom, "created_at":taim1}
            else: 
                nom = 5 + (0.3 * profile.number_people) 
                profile.balance_netbo += nom
                profile.save()
                username_id =str(profile.id)
                data = {"profile_id":username_id, 'balance_netbo':nom, "created_at":taim1}
            tran = Tranzaktionserialazer(data=data)
            profile.last_mining = int(time.time())
            profile.save()
            if tran.is_valid():
                tran.save()
            return Response({'message': 1, "transaction":tran.data},status=status.HTTP_200_OK)
        else:
            return Response({'message': -2},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_tr(request):
    if request.method == 'GET':
        tr = Transaction.objects.all()
        serializer = Tranzaktionserialazer(tr, many=True)
        return Response({'message': 1,"profile":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def balance_history(request, pk):
    if request.method == 'GET':
        current_timestamp = int(time.time())
        current_date = datetime.utcfromtimestamp(current_timestamp).date()

        dey_sum = 0
        days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
        moon_sum = [0] * days_in_month
        week_sum = [0] * 7
        profile = Profile.objects.get(id=pk)
        username_id = profile.id

        all_transactions = Transaction.objects.filter(profile_id=username_id)

        # Kunlik tranzaksiyalar
        daily_transactions = all_transactions.filter(
            created_at__gte=current_timestamp - 86400,
            created_at__lt=current_timestamp
        )
        dey_sum = daily_transactions.aggregate(Sum('balance_netbo'))['balance_netbo__sum'] or 0

        # Haftalik tranzaksiyalar
        weekly_transactions = all_transactions.filter(
            created_at__gte=current_timestamp - (86400 * 7),
            created_at__lt=current_timestamp
        )
        week_sum = [0] * 7  # Reset week_sum
        for transaction in weekly_transactions:
            transaction_date = datetime.utcfromtimestamp(transaction.created_at).date()
            day_of_week = transaction_date.weekday()
            week_sum[day_of_week] += transaction.balance_netbo

        # Oylik tranzaksiyalar
        oylik_transactions = all_transactions.filter(
            created_at__gte=current_timestamp - (86400 * days_in_month),
            created_at__lt=current_timestamp
        )
        moon_sum = [0] * days_in_month  # Reset moon_sum
        for transaction in oylik_transactions:
            transaction_date = datetime.utcfromtimestamp(transaction.created_at).date()
            day_of_month = transaction_date.day - 1
            moon_sum[day_of_month] += transaction.balance_netbo

        return Response({'message': 1, 'daily': dey_sum, "weekly": week_sum, 'monthly': moon_sum}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def get_tr_us(request, pk):
    if request.method == 'GET':
        try:
            tr = Transaction.objects.filter(profile_id=pk)
        except:
            return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)
        serialazer = UserTranzaktionserialazer(tr, many=True)
        return Response({'message': 1,"profile":serialazer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': -1},status=status.HTTP_400_BAD_REQUEST)
    