|
// [next->](0003-decision-3.md)

# 3. Seperate menuns from the app logic

Date: 2025-Mar-10

## Context

When using the CLI mode of the application, number based menus are used to natigate the app. The menu code is frequency repeated with some minor differences. So it is better to seperate the menu into separate class.

## Decision

Decided to make two classes `Menu` which handles displaying the menu and getting the users selection. And `MenuOption` which repersents one option, storing the display text and a value that is return when the option is selected.
