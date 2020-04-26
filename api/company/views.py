from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from company.serializers import CompanySerializer
from rest_framework.permissions import IsAdminUser
from company.models import Company


class CreateCompanyAPIView(CreateAPIView):
	''' Create Companies only Admin user can perform others can't do '''
	queryset = Company.objects.all()
	permission_classes = [IsAdminUser]
	serializer_class = CompanySerializer

	def create(self, request, *args, **kwargs):
		''' Add new company to the profile '''
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
			
		data = serializer.data
		headers = self.get_success_headers(serializer.data)
		return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class CompanyListAPIView(ListAPIView):
	''' View Companies only Admin user can able to manage others can't do '''
	queryset = Company.objects.all()
	serializer_class = CompanySerializer
	permission_classes = [IsAdminUser]

	def list(self, request):
		''' List out the companies and also can filter using name or location or both '''
		filters = {}
		for key, value in request.query_params.items():
			if key in ['name', 'location']:
				filters[key] = value
		queryset = self.get_queryset()
		if filters:
			queryset = queryset.filter(**filters)				
		serializer = CompanySerializer(queryset, read_only=True, many=True)
		return Response(serializer.data)


class UpdateCompanyAPIView(UpdateAPIView):
	''' Update Companies only Admin user can able to update others can't do '''
	queryset = Company.objects.all()
	serializer_class = CompanySerializer
	permission_classes = [IsAdminUser]

	def update(self, request, *args, **kwargs):
		''' update company profile  '''
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data)        
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)

class DestroyCompanyAPIView(DestroyAPIView):
	''' Destroy Companies only Admin user can able to update others can't do '''
	queryset = Company.objects.all()
	serializer_class = CompanySerializer
	permission_classes = [IsAdminUser]

	def destroy(self, request, *args, **kwargs):
		''' Delete the company '''
		instance = self.get_object()
		self.perform_destroy(instance)
		return Response(status=status.HTTP_204_NO_CONTENT)
		return super(DestroyCompanyAPIView, self).destroy(request, key, *args, **kwargs)