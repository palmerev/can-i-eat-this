# "Can I Eat This?"
_A food/diet/recipe journal and organization tool_

**VISION**: A tool that makes it easier to track cause and effect relationships between food and digestive quality, energy, weight, or whatever the user's goals are. CIET will (eventually) allow users to:
- develop customizable diet plans
- quickly see which foods are allowed, not allowed, or those that have restrictions or conditions, based on a particular diet plan (fully customizable with timestamped CRUD operations)
- log daily meals, along with any other pertinent notes (based on goals)
- store personal recipes, either links or as plaintext notes
- see foods ranked by popularity (based on meal logs), which could be helpful for seeing how balanced a diet is
- see a chronological history of their meal logs and notes

## Development Plan

Features will be implemented roughly in the order listed above:

1. Implement a user profile view and basic CRUD operations for custom diet plans
2. Implement the ability to search for particular diet plan, or see a food's status relative to a particular diet plan
3. Implement meal logging and notetaking
4. Implement food ranking based on log data
5. Implement a chronological history view based on log data

## Technologies

- Django/Python 3 (likely backed by PostgreSQL) OR possibly Ruby on Rails
- React and friends, with ES6/Babel
- HTML5/CSS3
- Webpack
- Mocha/Chai (unit testing)

--
_DISCLAIMER: This app does not and will not provide professional medical or nutrition advice, and does not substitute for such advice. It is intended only as an organizational tool to help users gather better data about their relationships with food._
