"""
Assignment 3: Real World Application of Loop Control Statements
Program: Simple Country World Cup 2026 Simulator

This program simulates a simple country that will win the World Cup 2026.
Uses a while loop to control the flow of the program and uses break, continue,
and pass statements to manage the flow of the loop based on user input.
"""

def world_cup_simulator():
    """
    Simulates a World Cup tournament where users compete to win.
    Demonstrates break, continue, and pass statements in a while loop.
    """
    
    print("=" * 70)
    print("WORLD CUP 2026 TOURNAMENT SIMULATOR")
    print("=" * 70)
    print("\nWelcome! This program simulates a World Cup tournament.")
    print("Help your country win the World Cup 2026!\n")
    
    # Get player name and country
    player_name = input("Enter your name: ").strip()
    country = input("Enter your country name: ").strip()
    
    if not player_name or not country:
        print("Invalid input. Using default values.")
        player_name = "Player"
        country = "Unknown Country"
    
    print(f"\n{player_name} representing {country}!")
    print("=" * 70)
    
    # Initialize game variables
    wins = 0
    matches_played = 0
    max_matches = 3
    total_goals = 0
    
    print(f"\nYour goal: Win {max_matches} matches to win the World Cup!")
    print("Commands: 'play', 'stats', 'quit'\n")
    
    # Main game loop
    while True:
        command = input(f"\n[Match {matches_played + 1}/{max_matches}] Enter command: ").strip().lower()
        
        # Break statement - exit the tournament
        if command == "quit":
            print(f"\n{'=' * 70}")
            print(f"Tournament ended. {country} is leaving the World Cup.")
            print(f"Final Statistics:")
            print(f"  Matches Played: {matches_played}")
            print(f"  Wins: {wins}")
            print(f"  Total Goals: {total_goals}")
            print("Thank you for playing!")
            print(f"{'=' * 70}\n")
            break
        
        # Continue statement - skip to next iteration if invalid command
        elif command == "stats":
            print(f"\n{'*' * 70}")
            print(f"TOURNAMENT STATISTICS FOR {country.upper()}")
            print(f"{'*' * 70}")
            print(f"Player Name: {player_name}")
            print(f"Country: {country}")
            print(f"Matches Played: {matches_played}")
            print(f"Wins: {wins}")
            print(f"Win Rate: {(wins/matches_played*100):.1f}%" if matches_played > 0 else "Win Rate: 0%")
            print(f"Total Goals Scored: {total_goals}")
            print(f"Goals Per Match: {(total_goals/matches_played):.1f}" if matches_played > 0 else "Goals Per Match: 0")
            print(f"{'*' * 70}")
            continue
        
        # Play command - simulate a match
        elif command == "play":
            if matches_played >= max_matches:
                print(f"\n{'!' * 70}")
                if wins >= max_matches:
                    print(f"🏆 CONGRATULATIONS! {country} WON THE WORLD CUP 2026! 🏆")
                    print(f"Player: {player_name} is now a World Cup Champion!")
                else:
                    print(f"{country} did not win the World Cup.")
                    print(f"You won {wins} out of {max_matches} matches.")
                    print("Better luck next tournament!")
                print(f"{'!' * 70}")
                break
            
            print(f"\n{'-' * 70}")
            print(f"MATCH {matches_played + 1}")
            print(f"{'-' * 70}")
            
            # Opponent selection
            opponents = ["Brazil", "France", "Germany", "Argentina", "Spain", "England", "Belgium", "Netherlands"]
            import random
            opponent = random.choice(opponents)
            
            print(f"{country} vs {opponent}")
            print("\nSimulating match...\n")
            
            # Simulate match outcome
            your_score = random.randint(0, 4)
            opponent_score = random.randint(0, 4)
            
            print(f"Final Score: {country} {your_score} - {opponent_score} {opponent}")
            
            matches_played += 1
            total_goals += your_score
            
            # Check match result
            if your_score > opponent_score:
                wins += 1
                print(f"✓ {country} WINS! Great performance by {player_name}!")
            elif your_score < opponent_score:
                print(f"✗ {country} LOSES. Better luck in the next match!")
            else:
                print(f"○ DRAW. Both teams played equally well.")
            
            # Pass statement - used as placeholder for potential future functionality
            if your_score >= 3:
                pass  # Could add additional logic here for outstanding performances
            
            print(f"{'-' * 70}")
            
            # Continue to next iteration after match
            continue
        
        else:
            print("❌ Invalid command! Use 'play', 'stats', or 'quit'.")
            continue


def advanced_tournament():
    """
    Advanced version with multiple rounds and knockout stages.
    Demonstrates nested while loops with break and continue statements.
    """
    
    print("\n" + "=" * 70)
    print("ADVANCED WORLD CUP 2026 - GROUP STAGE SIMULATOR")
    print("=" * 70 + "\n")
    
    player_name = input("Enter your name: ").strip()
    country = input("Enter your country name: ").strip()
    
    if not player_name or not country:
        player_name = "Player"
        country = "Unknown Country"
    
    print(f"\n{player_name} from {country} - Welcome to the Group Stage!\n")
    
    group_teams = [country, "Team A", "Team B", "Team C"]
    points = 0
    matches = 0
    max_group_matches = 3
    goals_for = 0
    goals_against = 0
    
    print(f"Your group: {', '.join(group_teams)}")
    print(f"Objective: Qualify from group stage (Top 2)\n")
    
    import random
    
    # Group stage loop
    group_stage = True
    while group_stage and matches < max_group_matches:
        action = input(f"\n[Group Match {matches + 1}] Play match? (yes/no/skip): ").strip().lower()
        
        if action == "skip":
            print("Skipping remaining matches. Check final standings.")
            break
        
        elif action == "no":
            continue
        
        elif action == "yes":
            opponent = random.choice([t for t in group_teams if t != country])
            your_goals = random.randint(0, 3)
            opp_goals = random.randint(0, 3)
            
            print(f"\n{country} {your_goals} - {opp_goals} {opponent}")
            
            goals_for += your_goals
            goals_against += opp_goals
            matches += 1
            
            if your_goals > opp_goals:
                points += 3
                print("✓ WIN (+3 points)")
            elif your_goals == opp_goals:
                points += 1
                print("○ DRAW (+1 point)")
            else:
                print("✗ LOSS (0 points)")
        
        else:
            print("Invalid command. Use 'yes', 'no', or 'skip'.")
            continue
    
    # Final group standings
    print(f"\n{'=' * 70}")
    print(f"GROUP STAGE FINAL STANDINGS")
    print(f"{'=' * 70}")
    print(f"Team: {country}")
    print(f"Matches Played: {matches}")
    print(f"Points: {points}")
    print(f"Goals For: {goals_for}")
    print(f"Goals Against: {goals_against}")
    print(f"Goal Difference: {goals_for - goals_against}")
    
    if points >= 5:
        print(f"\n🎉 {country} QUALIFIES FOR KNOCKOUT STAGE! 🎉")
    else:
        print(f"\n❌ {country} did not qualify. Better luck in 2030!")
    
    print(f"{'=' * 70}\n")


# Main execution
if __name__ == "__main__":
    while True:
        print("\nWORLD CUP 2026 TOURNAMENT MENU")
        print("=" * 70)
        print("1. Play Basic Tournament (Best of 3 matches)")
        print("2. Play Advanced Tournament (Group Stage)")
        print("3. Exit")
        print("=" * 70)
        
        choice = input("\nSelect mode (1, 2, or 3): ").strip()
        
        if choice == "1":
            world_cup_simulator()
        elif choice == "2":
            advanced_tournament()
        elif choice == "3":
            print("\nThank you for playing! Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")
            continue
