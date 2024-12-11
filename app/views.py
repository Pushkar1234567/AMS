from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterSerializer,UserSerializer, RosterSerializer, ShiftSerializer, AttendanceSerializer
from rest_framework.response import Response
from django.core.files.base import ContentFile
import base64
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Shift, Roster, Attendance
from django.utils.timezone import now
from datetime import timedelta,datetime

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Fix padding for Base64 string
def fix_base64_padding(encoded_str):
    return encoded_str + '=' * (-len(encoded_str) % 4)

class Register(APIView):
    permission_classes = [AllowAny] 

    
    def post(self,request):
        # print("inside the function")
        serializer = RegisterSerializer(data = request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                # print("data is ",serializer.data)
                return Response({"message":"User created successfully","data": serializer.data},status = 201)
            else:
                # print("data is ",serializer.data)
                return Response({"Error":"Something Wrong happens"},status = 201)
        except Exception as E:
            print("Error is : ",E)
            return Response({"Error":"Some Error occured"},status = 500)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Manager":
            raise PermissionDenied("Only managers can view the Users.")
        user = User.objects.filter(is_active = True)
        print("Users ::------ ",user)
        try:
            serializer = UserSerializer(user, many=True)
            print(serializer.data)
        except Exception as E:
            print("Error --- ",E)
        return Response(serializer.data)

    def put(self,request):
        if request.user.role != "Manager":
            raise PermissionDenied("Only managers can update the Users.")
        user_id = request.GET.get('id')
        user = User.objects.filter(id = user_id).first()
        serializer = UserSerializer(instance = user, data = request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message":"User Updated Successfully","data":serializer.data}, status = 200)
        else:
            
            return Response({"error":"Some error occur"}, status = 400)


class RosterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Manager":
            raise PermissionDenied("Only managers can view the roster.")
        rosters = Roster.objects.all()
        serializer = RosterSerializer(rosters, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "Manager":
            raise PermissionDenied("Only managers can create a roster.")
        print("request.data----- ",request.data)
        try:
            serializer = RosterSerializer(data=request.data)
        except Exception as E:
            print("Error---- ",E)
        if serializer.is_valid():
            serializer.save()
            

            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

    def put(self,request):
        if request.user.role != "Manager":
            raise PermissionDenied("Only managers can create a roster.")
        roster_id = request.GET.get('id')
        if not roster_id:
            return Response("Please provide roster_id in the params")
        roster = Roster.objects.filter(id = roster_id).first()
        serializer = RosterSerializer(instance = roster, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Roster Updated Successfully","data":serializer.data}, status = 200)
        else:
            return Response("Some error Occured",status = 400)


class ShiftView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Staff":
            raise PermissionDenied("Only staff can view shifts.")
        print("Roster id is : --- ",request.user.id)
        shift = Shift.objects.filter(staff_id = request.user.id).first()
        print(shift)
        serializer = ShiftSerializer(shift)
        return Response(serializer.data)


class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "Staff":
            raise PermissionDenied("Only staff can view attendance.")
        attendances = Attendance.objects.filter(staff=request.user)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "Staff":
            raise PermissionDenied("Only staff can mark attendance.")

        # Check for shift
        current_time = now()

        print(f"current time {current_time}, user {request.user.id}, day {current_time.strftime("%A")}")
        
        shift = Shift.objects.filter(
            staff_id=request.user.id,
        ).first()
        if not shift or current_time.strftime("%A") not in shift.day:
            return Response({"error": "No shift assigned for today."}, status=400)
        print("Shift is --- ", shift.day)

        shift = Shift.objects.filter(
            staff_id=request.user.id
        ).first()
        print("here is shift ---- ",shift.shift_time)

        # Parse shift timing
        # try:
        #     # Debug the value of shift_time
        #     print("Shift Time String:", shift.shift_time)

        #     # Split multiple shifts by comma
        #     shifts = shift.shift_time.split(",")
        #     parsed_shifts = []

        #     for shift_entry in shifts:
        #         shift_entry = shift_entry.strip()  # Remove any leading/trailing spaces
        #         parts = shift_entry.split(" - ", 1)  # Safely split into two parts
        #         if len(parts) != 2:
        #             raise ValueError(f"Invalid shift entry: {shift_entry}")

        #         start_time_str, end_time_str = parts
        #         shift_start_time = datetime.strptime(start_time_str.strip(), "%H:%M").time()
        #         shift_end_time = datetime.strptime(end_time_str.strip(), "%H:%M").time()
        #         parsed_shifts.append((shift_start_time, shift_end_time))

        #     # Debug the parsed shifts
        #     print("Parsed Shifts:", parsed_shifts)

        #     # Validate attendance window for any of the shifts
        #     current_time = now().time()
        #     is_within_allowed_window = False

        #     for shift_start_time, _ in parsed_shifts:
        #         # Calculate attendance window for this shift (1 hour before and 1 hour after shift start)
        #         allowed_start_time = (datetime.combine(now().date(), shift_start_time) -
        #                             timedelta(minutes=60)).time()
        #         allowed_end_time = (datetime.combine(now().date(), shift_start_time) +
        #                             timedelta(minutes=60)).time()

        #         print(f"Validating: Shift Start: {shift_start_time}, Allowed Start: {allowed_start_time}, Allowed End: {allowed_end_time}")

        #         # Check if current time falls within the window
        #         if allowed_start_time <= current_time <= allowed_end_time:
        #             is_within_allowed_window = True
        #             break

        #     if not is_within_allowed_window:
        #         return Response(
        #             {"error": "Attendance must be marked within 1 hour of a shift start time."},
        #             status=400
        #         )

        # except Exception as E:
        #     print("Error-- ",E)
        #     return Response({"error": "Invalid shift time format."}, status=400)

        
        try:
            # Get webcam data from request
            webcam_data = request.data.get("webcam")
            if not webcam_data or ";base64," not in webcam_data:
                return Response({"error": "Invalid webcam data."}, status=400)

            # Extract Base64 and file format
            format, imgstr = webcam_data.split(";base64,")
            ext = format.split("/")[-1]

            # Fix padding issue
            imgstr = fix_base64_padding(imgstr)

            # Decode Base64 image and create ContentFile
            image = ContentFile(base64.b64decode(imgstr), name=f"{request.user.id}_{now().strftime('%Y%m%d%H%M%S')}.{ext}")

            # Save attendance
            serializer = AttendanceSerializer(data={
                "staff": request.user.id,
                "image": image,
                "shift": shift.id,
            })
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

