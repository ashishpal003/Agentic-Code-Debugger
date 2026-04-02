from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

class Tracer:
    
    def __init__(self):
        provider = TracerProvider()
        processor = BatchSpanProcessor(ConsoleSpanExporter())

        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

        self.tracer = trace.get_tracer("debug-agent")

    def start_span(self, name):
        return self.tracer.start_as_current_span(name)