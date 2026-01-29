from darts import TimeSeries
from darts.models import TFTModel

def train_music_tft(data_frame):
    # Convertimos tu historial de YouTube Music en una serie temporal
    series = TimeSeries.from_dataframe(data_frame, 'timestamp', 'energy_score')
    
    model = TFTModel(
        input_chunk_length=24, # Mira las últimas 24 canciones
        output_chunk_length=5, # Predice la tendencia de las próximas 5
        n_epochs=20,
        random_state=42
    )
    model.fit(series)
    return model