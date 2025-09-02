#!/bin/bash
# Enhanced MissDorking Unix/Linux Launcher 💋
# With bulk domains, smart file naming, and fabulous CLI support! 🍒

# Color definitions for fabulous output
PINK='\033[95m'
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
CYAN='\033[96m'
WHITE='\033[97m'
RESET='\033[0m'
BOLD='\033[1m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to print banner
print_banner() {
    echo ""
    echo -e "${PINK}    💋 MissDorking™ Enhanced Unix/Linux Launcher 🍒${RESET}"
    echo -e "${CYAN}    ╔══════════════════════════════════════════════════╗${RESET}"
    echo -e "${CYAN}    ║  😘  Making Security Fun & Fabulous on Unix/Linux! 💅 ║${RESET}"
    echo -e "${CYAN}    ╚══════════════════════════════════════════════════╝${RESET}"
    echo ""
}

# Function to check virtual environment
check_venv() {
    if [ ! -f "venv/bin/activate" ]; then
        echo -e "${RED}❌ Virtual environment not found!${RESET}"
        echo -e "${YELLOW}💡 Run install_debian.sh first to set up the environment${RESET}"
        exit 1
    fi
}

# Function to activate virtual environment
activate_venv() {
    echo -e "${BLUE}🔧 Activating virtual environment...${RESET}"
    source venv/bin/activate
    
    # Check if activation was successful
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Failed to activate Python virtual environment${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Virtual environment activated successfully!${RESET}"
    echo ""
}

# Function to show main menu
show_menu() {
    echo -e "${PINK}💅 Choose your fabulous dorking mode:${RESET}"
    echo ""
    echo -e "${CYAN}[1]${RESET} 🎯 GUI Mode - Pretty interface for interactive dorking"
    echo -e "${CYAN}[2]${RESET} 👑 Enhanced GUI - Super-powered with bulk & fun features"  
    echo -e "${CYAN}[3]${RESET} ⚡ Super Fast GUI - Ludicrously optimized for speed demons"
    echo -e "${CYAN}[4]${RESET} 💻 CLI Mode - Command line for power users"
    echo -e "${CYAN}[5]${RESET} 📋 CLI Bulk Mode - Bulk domain processing via CLI"
    echo -e "${CYAN}[6]${RESET} 🎪 Fun Launcher - Full experience with splash & speed test"
    echo -e "${CYAN}[7]${RESET} 📊 Speed Test - Test the performance improvements"
    echo -e "${CYAN}[8]${RESET} ❓ Show CLI Help - Display command line options"
    echo -e "${CYAN}[9]${RESET} 🚪 Exit - Close this fabulous tool"
    echo ""
}

# Function to run GUI mode
run_gui_mode() {
    echo ""
    echo -e "${PINK}🎯 Starting original GUI mode...${RESET}"
    python3 main_gui.py 2>/dev/null || python main_gui.py
}

# Function to run enhanced GUI
run_enhanced_gui() {
    echo ""
    echo -e "${PINK}👑 Starting enhanced GUI with bulk domains...${RESET}"
    python3 main_gui_enhanced.py 2>/dev/null || python main_gui_enhanced.py
}

# Function to run super fast GUI
run_super_fast_gui() {
    echo ""
    echo -e "${PINK}⚡ Starting super fast optimized GUI...${RESET}"
    python3 super_fast_gui.py 2>/dev/null || python super_fast_gui.py
}

# Function to run CLI mode
run_cli_mode() {
    echo ""
    echo -e "${PINK}💻 CLI Mode - Single Domain Dorking${RESET}"
    echo ""
    
    read -p $'\033[96m🎯 Enter domain to scan: \033[0m' domain
    if [ -z "$domain" ]; then
        echo -e "${RED}❌ No domain specified${RESET}"
        return
    fi

    echo -e "${CYAN}⚙️ Scan Options:${RESET}"
    
    read -p $'\033[96m📊 Max results per query (default 10): \033[0m' max_results
    max_results=${max_results:-10}
    
    read -p $'\033[96m⏰ Delay range in seconds (default 2-4): \033[0m' delay
    delay=${delay:-"2-4"}
    
    read -p $'\033[96m⚡ Use hybrid scraper for better results? (y/n, default n): \033[0m' use_hybrid
    
    hybrid_flag=""
    if [[ "$use_hybrid" =~ ^[Yy]$ ]]; then
        hybrid_flag="--hybrid"
    fi

    echo ""
    echo -e "${GREEN}🚀 Starting CLI scan for $domain...${RESET}"
    python3 run_dorking_cli.py -d "$domain" --max-results "$max_results" --delay "$delay" $hybrid_flag --export pdf csv 2>/dev/null || \
    python run_dorking_cli.py -d "$domain" --max-results "$max_results" --delay "$delay" $hybrid_flag --export pdf csv
}

# Function to run bulk CLI mode
run_bulk_cli_mode() {
    echo ""
    echo -e "${PINK}👑 Bulk CLI Mode - Multiple Domain Domination${RESET}"
    echo ""
    echo -e "${CYAN}Choose bulk input method:${RESET}"
    echo -e "${CYAN}[1]${RESET} 📁 Load from file"
    echo -e "${CYAN}[2]${RESET} ✍️ Enter domains manually (comma-separated)"
    echo ""
    
    read -p $'\033[93m💋 Enter choice (1-2): \033[0m' bulk_choice

    case $bulk_choice in
        1)
            read -p $'\033[96m📁 Enter path to domains file: \033[0m' domains_file
            if [ ! -f "$domains_file" ]; then
                echo -e "${RED}❌ File not found: $domains_file${RESET}"
                return
            fi
            bulk_input="$domains_file"
            ;;
        2)
            read -p $'\033[96m✍️ Enter domains (comma-separated): \033[0m' bulk_input
            if [ -z "$bulk_input" ]; then
                echo -e "${RED}❌ No domains specified${RESET}"
                return
            fi
            ;;
        *)
            echo -e "${RED}❌ Invalid choice${RESET}"
            return
            ;;
    esac

    echo -e "${CYAN}📋 Report Format:${RESET}"
    echo -e "${CYAN}[1]${RESET} Individual reports per domain"
    echo -e "${CYAN}[2]${RESET} Single combined report for all"
    echo -e "${CYAN}[3]${RESET} Both individual and combined"
    echo ""
    
    read -p $'\033[93m💋 Enter choice (1-3): \033[0m' report_choice

    case $report_choice in
        1) report_format="individual" ;;
        2) report_format="combined" ;;
        3) report_format="both" ;;
        *) report_format="individual" ;;
    esac

    echo ""
    echo -e "${GREEN}🚀 Starting bulk CLI scan...${RESET}"
    python3 run_dorking_cli.py -b "$bulk_input" --report-format "$report_format" --export pdf csv 2>/dev/null || \
    python run_dorking_cli.py -b "$bulk_input" --report-format "$report_format" --export pdf csv
}

# Function to run fun launcher
run_fun_launcher() {
    echo ""
    echo -e "${PINK}🎪 Starting fun launcher with full experience...${RESET}"
    python3 launch_super_fast.py 2>/dev/null || python launch_super_fast.py
}

# Function to run speed test
run_speed_test() {
    echo ""
    echo -e "${PINK}📊 Running speed test...${RESET}"
    python3 speed_test.py 2>/dev/null || python speed_test.py
}

# Function to show CLI help
show_cli_help() {
    echo ""
    echo -e "${PINK}💻 MissDorking CLI Help ${RESET}"
    echo ""
    python3 run_dorking_cli.py --help 2>/dev/null || python run_dorking_cli.py --help
    echo ""
    read -p $'\033[93mPress Enter to continue...\033[0m'
}

# Function to handle completion
handle_completion() {
    echo ""
    echo -e "${GREEN}✨ MissDorking operation completed!${RESET}"
    echo ""
    read -p $'\033[93m💋 Return to main menu? (y/n): \033[0m' restart
    if [[ "$restart" =~ ^[Yy]$ ]]; then
        return 0  # Continue to main loop
    else
        echo -e "${PINK}💅 Goodbye, fabulous user! 💋${RESET}"
        exit 0
    fi
}

# Main script execution
main() {
    print_banner
    check_venv
    activate_venv

    while true; do
        show_menu
        read -p $'\033[93m💋 Enter your choice (1-9): \033[0m' choice

        case $choice in
            1)
                run_gui_mode
                handle_completion || continue
                ;;
            2)
                run_enhanced_gui
                handle_completion || continue
                ;;
            3)
                run_super_fast_gui
                handle_completion || continue
                ;;
            4)
                run_cli_mode
                handle_completion || continue
                ;;
            5)
                run_bulk_cli_mode
                handle_completion || continue
                ;;
            6)
                run_fun_launcher
                handle_completion || continue
                ;;
            7)
                run_speed_test
                handle_completion || continue
                ;;
            8)
                show_cli_help
                continue
                ;;
            9)
                echo ""
                echo -e "${PINK}💋 Thanks for using MissDorking! Stay fabulous! 🍒${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Invalid choice. Please enter 1-9.${RESET}"
                echo ""
                continue
                ;;
        esac
    done
}

# Handle script arguments for direct CLI usage
if [ $# -gt 0 ]; then
    check_venv
    activate_venv
    
    echo -e "${PINK}💻 Direct CLI mode activated${RESET}"
    python3 run_dorking_cli.py "$@" 2>/dev/null || python run_dorking_cli.py "$@"
else
    # Run interactive menu
    main
fi
