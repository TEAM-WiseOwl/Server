from django.shortcuts import render

class Notice(APIView):
  def get(self, request):
    basket = Basket_dream.objects.get(user_id=request.user_id)