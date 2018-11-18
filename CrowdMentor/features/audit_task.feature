Feature: Audit task

  Scenario: Auditor must be able to audit the task
    Given I am an existing user with task_updater access
    Given I am logged in as the user with task_updater access
    And I add a task to be audited
    And I logout
    And I am an existing user with auditor access
    And I am logged in as the user with auditor access