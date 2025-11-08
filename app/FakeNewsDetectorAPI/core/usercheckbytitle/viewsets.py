from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserCheckSerializer
from core.model import load_models
from core.llm import query_llm

class UserCheckViewSet(viewsets.ViewSet):
    """Viewset to handle user checking other news."""
    http_method_names = ('post', )
    serializer_class = UserCheckSerializer
    nb_model, vect_model = load_models()

    def create(self, request):
        """Get's news from user and returns predicted value."""
        serializer = UserCheckSerializer(data=request.data)
        if serializer.is_valid():
            input_text = serializer.validated_data['user_news']
            input_data = [input_text]
            vectorized_text = self.vect_model.transform(input_data)
            prediction = self.nb_model.predict(vectorized_text)
            prediction_bool = True if prediction[0] == 1 else False
            prompt = (
                f"Analyze this news headline: \"{input_text.strip()}\"\n\n"
                "Your task:\n"
                "1. First, clearly state if this headline is likely REAL or FAKE.\n"
                "2. Then provide a brief explanation (2-3 sentences) supporting your assessment.\n"
                "3. Explain what makes it credible or suspicious.\n\n"
                "Format your response as:\n"
                "Verdict: [REAL/FAKE]\n"
                "Explanation: [Your analysis here]\n\n"
                "Be concise and direct. Do not use bullet points."
            )

            analysis_text = None
            analysis_error = None
            if input_text.strip():
                success, message = query_llm(prompt)
                if success:
                    analysis_text = message
                else:
                    analysis_error = message

            response_data = {'prediction': prediction_bool}
            if analysis_text:
                response_data['analysis'] = analysis_text
            if analysis_error:
                response_data['analysis_error'] = analysis_error
            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)
