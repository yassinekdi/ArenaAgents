from ts.torch_handler.base_handler import BaseHandler
import json
import random

class RandomAgentHandler(BaseHandler):
    def initialize(self, context):
        self.initialized = True

    def preprocess(self, requests):
        data = requests[0].get("body")
        if isinstance(data, (bytes, bytearray)):
            data = data.decode('utf-8')
        return json.loads(data)


    def inference(self, data):
        player = data['player']
        game_context = data['game_context']
        
        # List of possible actions
        actions = [1, 2, 3, 4]  # 1: Fold, 2: Bet, 3: Check, 4: Call
        
        # Select a random action
        action_chosen = random.choice(actions)
        
        # Prepare the response
        response = {"action": action_chosen}
        
        # If the action is "Bet", determine a random bet amount
        if action_chosen == 2:
            max_bet = min(player['bankroll'], game_context['last_bet'] * 2)  # Example constraint
            if max_bet == 0:
                response['action'] = random.choice([1, 3, 4])  # Reassign action if no funds for betting
            else:
                response['amount'] = random.randint(game_context['last_bet'], max_bet)
        
        return [response]

    def postprocess(self, inference_output):
        # Convert the inference output to JSON string
        return [inference_output[0]]


