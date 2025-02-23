class EstrusDetectionView(generics.GenericAPIView):
    serializer_class = CowEstrusSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            model_path = os.path.join(settings.VARIABLE_ROOT, 'shared', 'aimodels', 'estrus_model_v1_state.pth')
            if not os.path.exists(model_path):
                model_path = os.path.join(settings.BASE_DIR, 'shared', 'aimodels', 'estrus_model_v1_state.pth')

            detector = EstrusDetector(model_path, PyTorchEstrusHandler())
            prediction = detector.detect()

            return Response({"prediction": prediction.tolist()})
        except Exception as e:
            return Response({"error": f"Prediction failed: {str(e)}"}, status=500)