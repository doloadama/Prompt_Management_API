# POJAT API-REST

## Project Overview

**Deadline: 30/07/2024**

### Objective

Develop a RESTful API using Flask to manage users and text prompts. The API will include features for handling user connections and authorizations.

## Functional Description

### Roles and Features

**Administrator:**
- Create individual users or user groups.
- Validate, request modifications, or delete prompts.
- View all prompts but cannot vote or rate them.

**Users:**
- Propose prompts for sale.
- Vote for the activation of pending prompts.
- Rate activated prompts but cannot vote or rate their own prompts.
- Members of the same group have a stronger impact on ratings and votes.

**Visitor (No login required):**
- View prompts.
- Search for prompts by content or keywords.
- Purchase prompts.

### Prompt Management

- Default price of a prompt is 1000 F CFA.
- Ratings range from -10 to +10.
- Group member ratings count for 60%.
- External member ratings count for 40%.
- Prompt prices are recalculated after each rating with the formula:
  `New price = 1000 * (1 + average rating)`.

### Prompt States

- **Pending:** When added by a user.
- **Active:** After validation by an administrator or by vote.
- **Review:** If an administrator requests modification.
- **Reminder:** If no action is taken by the administrator within two days of addition or a modification/deletion request.
- **To Delete:** When a user requests deletion of their own prompt.

### Prompt Management Processes

- Members can vote for the activation of prompts in the Reminder state.
- Group member votes count for 2 points.
- External member votes count for 1 point.
- Prompts are activated if they reach at least 6 points.
- Administrators can validate or delete prompts at any time.
- Users can request deletion of their own prompts, which then move to the To Delete state.
- Prompts in the To Delete state for more than a day without administrator action move to the Reminder state.

### Additional Features

- Users can view the details of each prompt.
- Once validated or deleted, a prompt can no longer be rated.

## Diagrams and Planning

### Wireframes

- Design interfaces for user and prompt management.
- Interface for prompt rating and voting.
- Administration interface for managing prompt states.

### Use Case Diagram

- Visualize interactions between users, administrators, and the system.
- Include main actions such as account creation, prompt management, rating, and voting.
![Capture d’écran du 2024-07-06 10-20-43.png](Capture%20d%E2%80%99%C3%A9cran%20du%202024-07-06%2010-20-43.png)


### Class Diagram

- Model main entities (User, Group, Prompt) and their relationships.
- Integrate prompt states and possible actions.

### Planning with Trello

- Create dashboards with sprints and User Stories (US).
- Organize tasks by priority: user management, prompt management, integration of rating rules, etc.

### API Development

- Implement REST Endpoints for managing users, groups, prompts, and their states.
- Handle authentication and authorization.

## Technical Requirements

- Use PostgreSQL for the database.
- Use SQL for queries.
- Use JWT for connection and authorization management.
- Test the API using Postman.