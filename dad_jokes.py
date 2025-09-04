"""
Dad Jokes Module for MissDorking™
Because even hackers need a good laugh! 😂
"""

import random
from datetime import datetime

class DadJokesManager:
    def __init__(self):
        """Initialize the Dad Jokes Manager with tech/hacking themed jokes"""
        
        # Dad jokes with tech/security themes
        self.jokes = [
            # Classic dad jokes with tech twist
            "Why don't hackers ever get lost? Because they always know their way around the NET! 🌐",
            "Why did the firewall break up with the antivirus? It said 'You're too controlling!' 🔥",
            "What do you call a sleeping bull at a computer? A bulldozer! 💻",
            "Why don't programmers like nature? It has too many bugs! 🐛",
            "How do you comfort a JavaScript bug? You console it! 😂",
            
            # Dorking specific jokes
            "Why did the Google dork go to therapy? It had too many search issues! 🔍",
            "What's a hacker's favorite type of music? Heavy METAL... Detection! 🎵",
            "Why don't SQL injections ever work at restaurants? Because they always sanitize their inputs! 🍽️",
            "What do you call a group of disorganized hackers? A DDoS-organized crime! 💥",
            "Why did the penetration tester break up with their girlfriend? She said they were too intrusive! 💔",
            
            # Tech support dad jokes
            "Why did the computer keep sneezing? It had a virus! 🤧",
            "How do you fix a broken website? With a CTRL-ALT-DEFEAT! ⌨️",
            "Why don't computers ever get tired? They take plenty of power NAPs! 😴",
            "What's the best thing about UDP jokes? I don't care if you get them! 📡",
            "Why did the developer go broke? Because they used up all their cache! 💸",
            
            # Security themed
            "Why don't hackers ever win at poker? Because they can't help but show their hand! 🃏",
            "What do you call a fake certificate? A PHONEY CA! 📜",
            "Why did the password go to the gym? It wanted to be STRONGER! 💪",
            "How does a hacker flirt? 'Are you WiFi? Because I'm feeling a connection!' 📶",
            "Why don't security experts make good comedians? Their jokes are always too CRYPTIC! 🔐",
            
            # More general tech dad jokes
            "Why did the robot go on a diet? It had a byte problem! 🤖",
            "What do you call a computer superhero? A SCREEN saver! 🦸‍♂️",
            "Why was the smartphone wearing glasses? It lost its contacts! 👓",
            "How do you organize a space party? You planet in the CLOUD! ☁️",
            "Why don't keyboards ever get lonely? Because they have lots of FRIENDS! ⌨️",
            
            # Bonus cyber jokes
            "What's a hacker's favorite vegetable? A LEEK! 🥬",
            "Why did the cybersecurity expert refuse dessert? They were watching their COOKIES! 🍪",
            "How do hackers stay cool? They open WINDOWS! 🪟",
            "Why don't malware authors make good DJs? They always drop the PAYLOAD! 🎧",
            "What do you call a cat who works in IT? A PURR-ogrammer! 🐱"
        ]
        
        # Motivational tech quotes with dad joke twist
        self.motivational_jokes = [
            "Remember: If at first you don't succeed, try turning it off and on again! 🔌",
            "Today's forecast: 99% chance of debugging with scattered solutions! ☀️",
            "You're like good encryption - complex, secure, and impossible to crack! 💎",
            "Keep calm and sudo on! 👑",
            "Error 404: Monday motivation not found. Please try coffee! ☕",
            "You're not a bug, you're a FEATURE! ⭐",
            "Life is like code - even when it's messy, it can still work beautifully! 💖",
            "Stay positive like a proton, but keep your electrons close! ⚛️"
        ]
        
        # Special occasion jokes
        self.time_based_jokes = {
            'morning': [
                "Good morning! Time to brew some coffee and debug some dreams! ☕",
                "Rise and shine! Your computer missed you... it kept asking 'Are you sleeping?' 😴",
                "Morning motivation: You're like a fresh install - full of potential! 🌅"
            ],
            'afternoon': [
                "Afternoon energy boost: Remember, you're faster than Internet Explorer! 🚀",
                "Lunch break joke: Why do programmers prefer dark mode? Because light attracts bugs! 🌞",
                "Midday reminder: You're handling more processes than Task Manager! 💻"
            ],
            'evening': [
                "Evening wrap-up: You've debugged another day successfully! 🌆",
                "End of day wisdom: Save your work and save your sanity! 💾",
                "Evening joke: What's the best part about working from home? The commute is just a few clicks! 🏠"
            ]
        }
        
        self.current_joke_index = 0
        self.last_joke_time = datetime.now()
    
    def get_random_joke(self):
        """Get a random dad joke"""
        return random.choice(self.jokes)
    
    def get_motivational_joke(self):
        """Get a motivational tech joke"""
        return random.choice(self.motivational_jokes)
    
    def get_time_based_joke(self):
        """Get a joke based on current time of day"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            time_period = 'morning'
        elif 12 <= current_hour < 17:
            time_period = 'afternoon'
        else:
            time_period = 'evening'
        
        return random.choice(self.time_based_jokes[time_period])
    
    def get_sequential_joke(self):
        """Get jokes in sequence to avoid too much repetition"""
        joke = self.jokes[self.current_joke_index]
        self.current_joke_index = (self.current_joke_index + 1) % len(self.jokes)
        return joke
    
    def get_smart_joke(self):
        """Get a contextually appropriate joke"""
        now = datetime.now()
        
        # Show time-based jokes less frequently
        if random.random() < 0.3:  # 30% chance for time-based
            return self.get_time_based_joke()
        elif random.random() < 0.5:  # 50% chance for motivational
            return self.get_motivational_joke()
        else:  # Regular joke
            return self.get_random_joke()
    
    def get_startup_joke(self):
        """Special joke for app startup"""
        startup_jokes = [
            "Welcome back! I've been here debugging reality while you were away! 🤖",
            "Booting up... Dad joke engine initialized successfully! ✅",
            "System online! Ready to crack jokes and crack systems! 💪",
            "Loading complete! I missed you more than Windows misses your updates! 💙",
            "Ready to rock! Let's make some digital magic happen! ✨"
        ]
        return random.choice(startup_jokes)
    
    def get_export_joke(self):
        """Special jokes for export operations"""
        export_jokes = [
            "Exporting faster than my dad's tech support stories! 🚀",
            "PDF creation in progress... Adding extra dad joke compression! 📄",
            "CSV export loading... Now with 100% more spreadsheet humor! 📊",
            "File generation complete! It's more organized than my sock drawer! 🧦",
            "Export successful! This file is so good, it should have its own documentation! 📚"
        ]
        return random.choice(export_jokes)
    
    def get_scan_joke(self):
        """Special jokes for scanning operations"""
        scan_jokes = [
            "Scanning in progress... Like a dad looking for the TV remote! 🔍",
            "Dorking commenced! We're being more thorough than mom checking homework! 📝",
            "Search engines working harder than dad trying to assemble IKEA furniture! 🔧",
            "Results incoming! More findings than dad's 'helpful' suggestions! 💡",
            "Scan complete! We found more than dad finds in his junk drawer! 🗃️"
        ]
        return random.choice(scan_jokes)
    
    def get_progress_joke(self, progress_percentage):
        """Get jokes based on progress"""
        if progress_percentage < 25:
            return "Just getting started... Like dad with a new gadget! 📱"
        elif progress_percentage < 50:
            return "Making progress... Faster than dad learning TikTok! 📹"
        elif progress_percentage < 75:
            return "Almost there... Like dad 'almost' finishing that home project! 🏠"
        else:
            return "Nearly done... Like dad's story that's been going for 20 minutes! 📚"


# Convenience functions for easy access
dad_jokes = DadJokesManager()

def get_joke():
    """Quick access to get any joke"""
    return dad_jokes.get_smart_joke()

def get_startup_message():
    """Get a startup joke"""
    return dad_jokes.get_startup_joke()

def get_export_message():
    """Get an export-themed joke"""
    return dad_jokes.get_export_joke()

def get_scan_message():
    """Get a scan-themed joke"""
    return dad_jokes.get_scan_joke()

def get_progress_message(percentage):
    """Get a progress-based joke"""
    return dad_jokes.get_progress_joke(percentage)

# Test the module
if __name__ == "__main__":
    print("🎭 Dad Jokes Module Test:")
    print("-" * 50)
    
    # Test different types of jokes
    print("Random joke:", dad_jokes.get_random_joke())
    print("Motivational:", dad_jokes.get_motivational_joke())
    print("Time-based:", dad_jokes.get_time_based_joke())
    print("Startup:", dad_jokes.get_startup_joke())
    print("Export:", dad_jokes.get_export_joke())
    print("Scan:", dad_jokes.get_scan_joke())
    print("Progress:", dad_jokes.get_progress_joke(50))
