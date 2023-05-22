from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.queue import RabbitMQ
from diagrams.azure.compute import AppServices;
from diagrams.programming.language import Nodejs;
#Logic is defined in a singla place, easier to mandain
#Central traffic gateway - easier monitoring and logging
#Mediator/Orchestration Topology -> when there's a central component knowing all, like a central command to send all events
with Diagram("Event Driven - Mediator/Orchestration Topology", show=False, filename="big_picture_mediator", direction="TB"):
    with Cluster("Kubernetes"):   
        with Cluster("cooking_image"):
            cooking_service = AppServices("cooking_service")
        with Cluster("channel"):
            queue = RabbitMQ("cooking_queue")
        with Cluster("pickle_image"):
            pickle = AppServices("pickle_service")
        with Cluster("cheese_image"):
            cheese = AppServices("cheese_service")
        with Cluster("steak_image"):
            steak = AppServices("steak_service")
        with Cluster("app_queue", direction="LR"):
            cheese_queue = RabbitMQ("cheese_queue")
        with Cluster("app_queue", direction="LR"):
            steak_queue = RabbitMQ("steak_queue")
        with Cluster("app_queue", direction="LR"):
            pickle_queue = RabbitMQ("pickle_queue")
        with Cluster("consumer_service", direction="LR"):
            waiter = Nodejs("cook_app")

    workers = [pickle, cheese, steak]
    
    cooking_service >> queue >> workers
    cheese >> cheese_queue
    steak >> steak_queue
    pickle >> pickle_queue

    queues = [cheese_queue, steak_queue, pickle_queue]
    queues >> waiter