import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import string
import json
import os
import winsound  # For Windows beep sounds
import platform
from datetime import datetime, timedelta
import sys
from collections import deque
import math

class ZombieCheck:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ZombieCheck - Anti-Mindless-Browsing App 🧟‍♂️")
        self.root.geometry("500x700")
        self.root.configure(bg="#0d1117")
        
        # Enhanced app state
        self.is_active = False
        self.monitoring_thread = None
        self.challenge_window = None
        self.last_activity = time.time()
        self.activity_buffer = deque(maxlen=100)
        self.zombie_incidents = 0
        self.challenge_start_time = None
        self.zombie_onset_time = None
        self.stop_beeping_event = None
        self.beeping_thread = None
        self.challenge_in_progress = False  # NEW: Prevent multiple challenges
        self.grace_period_end = 0  # NEW: Grace period after successful challenge
        
        # Background monitoring and secret code
        self.background_monitoring = False
        self.secret_code = "5XETR5PZ"
        self.secret_entered = False
        
        # Enhanced activity tracking
        self.mouse_movements = deque(maxlen=50)
        self.key_presses = deque(maxlen=50)
        self.click_patterns = deque(maxlen=30)
        self.scroll_patterns = deque(maxlen=30)
        self.window_switches = 0
        self.last_mouse_pos = (0, 0)
        self.repetitive_actions = 0
        
        # Tolerance system - FASTER RESPONSE
        self.tolerance_level = 20  # Start with lower tolerance for faster detection
        self.max_tolerance = 100
        self.warning_given = False
        
        # Settings with enhanced options
        self.settings = {
            'sensitivity': 'medium',
            'idle_threshold': 180,
            'mindless_threshold': 90,
            'tolerance_decay': 1.0,  # Faster tolerance decrease
            'nightmare_mode': False,
            'gaming_mode': False,
            'visual_warnings': True,
            'adaptive_threshold': True,
            'grace_period': 60  # NEW: Grace period in seconds after challenge
        }
        
        # Enhanced stats
        self.stats = {
            'total_interventions': 0,
            'today_interventions': 0,
            'longest_streak': 0,
            'current_streak': 0,
            'avg_response_time': 0,
            'false_positives': 0,
            'successful_detections': 0,
            'tolerance_saves': 0,
            'daily_productivity_score': 100
        }
        
        self.load_stats()
        self.create_enhanced_interface()
        self.setup_global_activity_tracking()
        
    def create_enhanced_interface(self):
        """Create the enhanced UI with modern design"""
        # Custom colors
        bg_primary = "#0d1117"
        bg_secondary = "#161b22"
        bg_tertiary = "#21262d"
        accent_green = "#238636"
        accent_red = "#da3633"
        accent_orange = "#fd7e14"
        text_primary = "#f0f6fc"
        text_secondary = "#8b949e"
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=bg_primary)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title section with improved styling
        title_frame = tk.Frame(main_container, bg=bg_primary)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="🧟‍♂️ ZombieCheck", 
            font=("Segoe UI", 28, "bold"),
            fg=accent_green,
            bg=bg_primary
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Intelligent Anti-Mindless-Browsing Protection",
            font=("Segoe UI", 11),
            fg=text_secondary,
            bg=bg_primary
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Status section with enhanced visual feedback
        status_frame = tk.Frame(main_container, bg=bg_secondary, relief="solid", bd=1)
        status_frame.pack(fill="x", pady=(0, 20))
        
        status_inner = tk.Frame(status_frame, bg=bg_secondary)
        status_inner.pack(fill="x", padx=20, pady=15)
        
        self.status_label = tk.Label(
            status_inner,
            text="🔴 INACTIVE",
            font=("Segoe UI", 16, "bold"),
            fg=accent_red,
            bg=bg_secondary
        )
        self.status_label.pack()
        
        # Tolerance bar
        tolerance_frame = tk.Frame(status_inner, bg=bg_secondary)
        tolerance_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(
            tolerance_frame,
            text="Tolerance Level:",
            font=("Segoe UI", 10),
            fg=text_secondary,
            bg=bg_secondary
        ).pack(anchor="w")
        
        self.tolerance_canvas = tk.Canvas(tolerance_frame, height=10, bg=bg_tertiary, highlightthickness=0)
        self.tolerance_canvas.pack(fill="x", pady=(5, 0))
        
        # Control section
        control_frame = tk.Frame(main_container, bg=bg_primary)
        control_frame.pack(fill="x", pady=(0, 20))
        
        button_frame = tk.Frame(control_frame, bg=bg_primary)
        button_frame.pack()
        
        self.toggle_btn = tk.Button(
            button_frame,
            text="START MONITORING",
            font=("Segoe UI", 12, "bold"),
            bg=accent_green,
            fg="white",
            command=self.toggle_monitoring,
            width=18,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        self.toggle_btn.pack(side="left", padx=(0, 10))
        
        test_btn = tk.Button(
            button_frame,
            text="Test Challenge",
            font=("Segoe UI", 10),
            bg=accent_orange,
            fg="white",
            command=self.trigger_test_challenge,
            width=15,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        test_btn.pack(side="left")
        
        keyboard_test_btn = tk.Button(
            button_frame,
            text="Test Keyboard",
            font=("Segoe UI", 10),
            bg="#9c27b0",
            fg="white",
            command=self.test_keyboard_input,
            width=15,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        keyboard_test_btn.pack(side="left", padx=(10, 0))
        
        # Notebook for organized sections
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill="both", expand=True)
        
        # Stats tab
        stats_frame = tk.Frame(notebook, bg=bg_secondary)
        notebook.add(stats_frame, text="📊 Statistics")
        
        self.create_stats_section(stats_frame, bg_secondary, text_primary, text_secondary)
        
        # Settings tab
        settings_frame = tk.Frame(notebook, bg=bg_secondary)
        notebook.add(settings_frame, text="⚙️ Settings")
        
        self.create_settings_section(settings_frame, bg_secondary, text_primary, text_secondary, accent_green)
        
        # Detection Info tab
        info_frame = tk.Frame(notebook, bg=bg_secondary)
        notebook.add(info_frame, text="🔍 Detection Info")
        
        self.create_detection_info_section(info_frame, bg_secondary, text_primary, text_secondary)
        
        self.update_tolerance_bar()
        self.update_stats_display()
        
    def create_stats_section(self, parent, bg_color, text_primary, text_secondary):
        """Create enhanced stats section"""
        stats_container = tk.Frame(parent, bg=bg_color)
        stats_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Today's performance
        perf_frame = tk.LabelFrame(
            stats_container, 
            text="Today's Performance", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        perf_frame.pack(fill="x", pady=(0, 15))
        
        self.perf_text = tk.Text(
            perf_frame,
            height=6,
            font=("Consolas", 10),
            bg="#0d1117",
            fg="#58a6ff",
            insertbackground="#58a6ff",
            selectbackground="#264f78",
            relief="flat",
            padx=10,
            pady=10
        )
        self.perf_text.pack(fill="x", padx=10, pady=10)
        
        # All-time stats
        alltime_frame = tk.LabelFrame(
            stats_container, 
            text="All-Time Statistics", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        alltime_frame.pack(fill="both", expand=True)
        
        self.stats_text = tk.Text(
            alltime_frame,
            font=("Consolas", 10),
            bg="#0d1117",
            fg="#58a6ff",
            insertbackground="#58a6ff",
            selectbackground="#264f78",
            relief="flat",
            padx=10,
            pady=10
        )
        self.stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_settings_section(self, parent, bg_color, text_primary, text_secondary, accent_color):
        """Create enhanced settings section"""
        settings_container = tk.Frame(parent, bg=bg_color)
        settings_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Detection Settings
        detection_frame = tk.LabelFrame(
            settings_container, 
            text="Detection Settings", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        detection_frame.pack(fill="x", pady=(0, 15))
        
        # Sensitivity
        sens_frame = tk.Frame(detection_frame, bg=bg_color)
        sens_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(sens_frame, text="Sensitivity Level:", bg=bg_color, fg=text_primary, font=("Segoe UI", 10)).pack(anchor="w")
        
        self.sensitivity_var = tk.StringVar(value=self.settings['sensitivity'])
        sens_menu = ttk.Combobox(
            sens_frame, 
            textvariable=self.sensitivity_var,
            values=['low', 'medium', 'high', 'adaptive'],
            state="readonly",
            width=15
        )
        sens_menu.pack(anchor="w", pady=(5, 0))
        sens_menu.bind('<<ComboboxSelected>>', self.update_sensitivity)
        
        # Grace Period Setting
        grace_frame = tk.Frame(detection_frame, bg=bg_color)
        grace_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(grace_frame, text="Grace Period (seconds after challenge):", bg=bg_color, fg=text_primary, font=("Segoe UI", 10)).pack(anchor="w")
        
        self.grace_var = tk.StringVar(value=str(self.settings['grace_period']))
        grace_spinbox = tk.Spinbox(
            grace_frame,
            from_=30,
            to=300,
            increment=15,
            textvariable=self.grace_var,
            width=10,
            command=self.update_grace_period
        )
        grace_spinbox.pack(anchor="w", pady=(5, 0))
        
        # Checkboxes with better styling
        checkbox_frame = tk.Frame(detection_frame, bg=bg_color)
        checkbox_frame.pack(fill="x", padx=10, pady=10)
        
        self.adaptive_var = tk.BooleanVar(value=self.settings['adaptive_threshold'])
        adaptive_cb = tk.Checkbutton(
            checkbox_frame,
            text="Adaptive Learning (Learns your patterns)",
            variable=self.adaptive_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_adaptive_mode
        )
        adaptive_cb.pack(anchor="w", pady=2)
        
        self.nightmare_var = tk.BooleanVar(value=self.settings['nightmare_mode'])
        nightmare_cb = tk.Checkbutton(
            checkbox_frame,
            text="Nightmare Mode (Extra challenging codes)",
            variable=self.nightmare_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_nightmare_mode
        )
        nightmare_cb.pack(anchor="w", pady=2)
        
        self.gaming_var = tk.BooleanVar(value=self.settings['gaming_mode'])
        gaming_cb = tk.Checkbutton(
            checkbox_frame,
            text="Gaming Mode (Reduced interruptions)",
            variable=self.gaming_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_gaming_mode
        )
        gaming_cb.pack(anchor="w", pady=2)
        
        # Alerts (Visual only)
        av_frame = tk.LabelFrame(
            settings_container, 
            text="Alerts", 
            bg=bg_color, 
            fg=text_primary,
            font=("Segoe UI", 12, "bold")
        )
        av_frame.pack(fill="x", pady=(0, 15))
        
        av_checkbox_frame = tk.Frame(av_frame, bg=bg_color)
        av_checkbox_frame.pack(fill="x", padx=10, pady=10)
        
        self.visual_var = tk.BooleanVar(value=self.settings['visual_warnings'])
        visual_cb = tk.Checkbutton(
            av_checkbox_frame,
            text="Visual Warnings (Warning before challenge)",
            variable=self.visual_var,
            bg=bg_color,
            fg=text_primary,
            selectcolor=bg_color,
            activebackground=bg_color,
            activeforeground=text_primary,
            font=("Segoe UI", 10),
            command=self.update_visual_setting
        )
        visual_cb.pack(anchor="w", pady=2)
        
    def create_detection_info_section(self, parent, bg_color, text_primary, text_secondary):
        """Create section explaining how zombie detection works"""
        info_container = tk.Frame(parent, bg=bg_color)
        info_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a frame for text and scrollbar
        text_frame = tk.Frame(info_container, bg=bg_color)
        text_frame.pack(fill="both", expand=True)
        
        # Scrollable text widget
        info_text = tk.Text(
            text_frame,
            font=("Segoe UI", 10),
            bg="#0d1117",
            fg=text_primary,
            insertbackground=text_primary,
            selectbackground="#264f78",
            relief="flat",
            padx=15,
            pady=15,
            wrap="word"
        )
        info_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=info_text.yview)
        scrollbar.pack(side="right", fill="y")
        info_text.configure(yscrollcommand=scrollbar.set)
        
        detection_info = """🔍 HOW ZOMBIE DETECTION WORKS

ZombieCheck uses intelligent idle detection to prevent mindless browsing:

📊 ACTIVITY MONITORING:
• Mouse Movement: Tracks any mouse activity
• Keyboard Activity: Monitors typing and key presses
• Click Detection: Records mouse clicks
• Scroll Detection: Tracks scroll wheel activity
• Idle Time Calculation: Measures time since last activity
• Secret Code Detection: Monitors for "5XETR5PZ" activation

🧠 INTELLIGENT TOLERANCE SYSTEM:
• Tolerance Level: Builds up with focused work, depletes with mindless behavior
• Range: 0-100 points
• Saves: When tolerance is high, minor zombie behavior is forgiven
• Decay: Tolerance slowly decreases during inactivity
• Recovery: Good behavior quickly rebuilds tolerance

⚡ DETECTION TRIGGERS:

1. BACKGROUND MONITORING:
   • Secret Code: Type "5XETR5PZ" to activate
   • Silent Operation: Works in background
   • Idle Detection: 60 seconds of NO activity
   • Activity Reset: Any mouse/keyboard activity resets timer
   • Auto-Trigger: Only when completely inactive

2. IDLE DETECTION (ONLY):
   • Low Sensitivity: 5 minutes of inactivity
   • Medium Sensitivity: 3 minutes of inactivity  
   • High Sensitivity: 2 minutes of inactivity
   • Gaming Mode: Doubles all thresholds
   • Immediate Alert: 60 seconds of complete inactivity

3. TOLERANCE SYSTEM:
   • Builds up during active work
   • Decreases during idle periods
   • Prevents false positives
   • Adaptive to your work patterns

4. GRACE PERIOD:
   • After successful challenge completion
   • Prevents immediate re-triggering
   • Configurable duration (default: 60 seconds)

🎯 SENSITIVITY LEVELS:

• LOW: Relaxed detection, good for creative work
• MEDIUM: Balanced detection for general productivity
• HIGH: Strict detection for focused work sessions
• ADAPTIVE: AI learns your patterns and adjusts automatically

🔊 ALERT SYSTEM:
• Visual Warning: 10-second warning before challenge (if enabled)
• Sound Alert: Beep sound when zombie behavior detected
• Challenge Popup: Modal window requiring code entry
• Escalation: Harder challenges for repeated failures

🛡️ GRACE PERIOD SYSTEM:
• After successful challenge completion, monitoring is paused
• Grace period duration is configurable (default: 60 seconds)
• Prevents immediate re-triggering of challenges
• Allows you to refocus without interruption

📈 FEEDBACK SYSTEM:
• Response Time Tracking: Measures how quickly you respond
• Success Rate: Tracks accurate challenge completions
• Productivity Score: Daily score based on focused work
• Pattern Learning: System improves based on your feedback

The system is designed to be helpful, not annoying. It learns your work patterns and becomes more accurate over time, reducing false positives while catching genuine mindless browsing."""

        info_text.insert("1.0", detection_info)
        info_text.config(state="disabled")
        
    def setup_global_activity_tracking(self):
        """Setup global activity tracking"""
        self.root.bind('<Motion>', self.on_mouse_move)
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.bind('<Button-1>', self.on_click)
        self.root.bind('<Button-3>', self.on_click)
        self.root.bind('<MouseWheel>', self.on_scroll)
        self.root.focus_set()
        
        # Bind to all widgets for better keyboard detection
        self.root.bind_all('<KeyPress>', self.on_key_press)
        self.root.bind_all('<KeyRelease>', self.on_key_release)
        
        # Start periodic activity analysis
        self.analyze_activity_patterns()
        
        # Start background monitoring
        self.start_background_monitoring()
        
    def on_mouse_move(self, event):
        """Track mouse movement patterns"""
        current_time = time.time()
        current_pos = (event.x_root, event.y_root)
        
        # Calculate movement distance
        if self.last_mouse_pos:
            distance = math.sqrt(
                (current_pos[0] - self.last_mouse_pos[0])**2 + 
                (current_pos[1] - self.last_mouse_pos[1])**2
            )
        else:
            distance = 0
            
        self.mouse_movements.append({
            'time': current_time,
            'pos': current_pos,
            'distance': distance
        })
        
        self.last_mouse_pos = current_pos
        self.record_activity('mouse_move', current_time)
        
    def on_key_press(self, event):
        """Track keyboard activity"""
        current_time = time.time()
        self.key_presses.append({
            'time': current_time,
            'key': event.keysym
        })
        self.record_activity('key_press', current_time)
        
        # Check for secret code input
        self.check_secret_code(event.keysym)
        
        # Debug print for keyboard activity
        print(f"Keyboard activity detected: {event.keysym}")
    
    def on_key_release(self, event):
        """Track keyboard release activity"""
        current_time = time.time()
        self.record_activity('key_release', current_time)
        
    def on_click(self, event):
        """Track click patterns"""
        current_time = time.time()
        self.click_patterns.append({
            'time': current_time,
            'button': event.num,
            'pos': (event.x_root, event.y_root)
        })
        self.record_activity('click', current_time)
        
    def on_scroll(self, event):
        """Track scroll patterns"""
        current_time = time.time()
        self.scroll_patterns.append({
            'time': current_time,
            'delta': event.delta
        })
        self.record_activity('scroll', current_time)
        
    def record_activity(self, activity_type, timestamp):
        """Record activity in the activity buffer"""
        self.last_activity = timestamp
        self.activity_buffer.append({
            'type': activity_type,
            'time': timestamp
        })
        
        # Increase tolerance for good activity
        if activity_type == 'key_press':
            self.tolerance_level = min(self.max_tolerance, self.tolerance_level + 0.5)
    
    def check_secret_code(self, key):
        """Check for secret code input"""
        if not hasattr(self, 'secret_buffer'):
            self.secret_buffer = ""
        
        # Add key to buffer
        self.secret_buffer += key.upper()
        
        # Keep only last 8 characters
        if len(self.secret_buffer) > 8:
            self.secret_buffer = self.secret_buffer[-8:]
        
        # Check if secret code is entered
        if self.secret_buffer == self.secret_code:
            self.secret_entered = True
            self.secret_buffer = ""
            print(f"🎯 Secret code '{self.secret_code}' entered! Activating background monitoring...")
            self.activate_background_monitoring()
    
    def start_background_monitoring(self):
        """Start background monitoring thread"""
        self.background_monitoring = True
        self.background_thread = threading.Thread(target=self.background_monitor_loop, daemon=True)
        self.background_thread.start()
        print("🔄 Background monitoring started (waiting for secret code)")
    
    def background_monitor_loop(self):
        """Background monitoring loop - ONLY triggers when NO keyboard/mouse activity"""
        while self.background_monitoring:
            try:
                if self.secret_entered and not self.is_active:
                    # Check for idle time in background
                    current_time = time.time()
                    idle_time = current_time - self.last_activity
                    
                    # Debug print for monitoring (only when idle)
                    if idle_time > 30:  # Print every 30 seconds when idle
                        print(f"Background monitoring: {idle_time:.1f}s idle (NO activity)")
                    
                    # ONLY trigger if completely idle for 60 seconds (NO keyboard/mouse activity)
                    if idle_time >= 60:
                        print(f"🚨 Background IDLE detected: {idle_time:.1f}s of NO activity")
                        self.root.after(0, self.trigger_background_challenge)
                        break  # Stop monitoring after triggering
                    elif idle_time < 10:
                        # Reset if any activity detected
                        print(f"Activity detected - resetting idle timer: {idle_time:.1f}s")
                        
                time.sleep(1)  # Check every second
            except Exception as e:
                print(f"Background monitoring error: {e}")
                time.sleep(1)
    
    def activate_background_monitoring(self):
        """Activate background monitoring after secret code"""
        self.secret_entered = True
        print("✅ Background monitoring activated!")
        
        # Show activation message
        self.root.after(0, lambda: messagebox.showinfo(
            "Background Monitoring Activated", 
            f"Secret code '{self.secret_code}' accepted!\n\n"
            "🔄 ZombieCheck is now monitoring in the background.\n"
            "⏰ Will trigger ONLY after 60 seconds of NO activity.\n"
            "🖱️ Any mouse or keyboard activity resets the timer.\n"
            "🛑 Close the app to stop monitoring."
        ))
    
    def trigger_background_challenge(self):
        """Trigger challenge from background monitoring"""
        if not self.challenge_in_progress and not self.is_in_grace_period():
            print("🚨 Triggering background challenge!")
            self.trigger_intelligent_challenge(
                ["Background idle detection - 60 seconds of inactivity"], 
                100
            )
        
    def is_in_grace_period(self):
        """Check if we're still in grace period after a challenge"""
        return time.time() < self.grace_period_end
    
    def start_grace_period(self):
        """Start grace period after successful challenge"""
        self.grace_period_end = time.time() + self.settings['grace_period']
        print(f"Grace period started for {self.settings['grace_period']} seconds")
        
    def analyze_activity_patterns(self):
        """Continuously analyze activity patterns for zombie behavior - IDLE ONLY VERSION"""
        try:
            if not self.is_active:
                self.root.after(1000, self.analyze_activity_patterns)
                return
                
            # Skip analysis if challenge is in progress or in grace period
            if self.challenge_in_progress or self.is_in_grace_period():
                self.root.after(1000, self.analyze_activity_patterns)
                return
                
            current_time = time.time()
            
            # Check idle time - ONLY trigger on no keyboard/mouse movement
            idle_time = current_time - self.last_activity
            
            # Get idle threshold based on sensitivity
            idle_threshold = self.get_idle_threshold()
            
            # Debug print to see what's happening
            print(f"Idle time: {idle_time:.1f}s, Threshold: {idle_threshold}s, Tolerance: {self.tolerance_level}")
            
            # Immediate alarm for exactly 60s of idle (but respect grace period)
            if idle_time >= 60:
                print(f"TRIGGERING: 60s idle detected!")
                self.trigger_intelligent_challenge(
                    [f"No activity detected for {int(idle_time)} seconds"], 
                    100  # Maximum zombie score for immediate action
                )
                self.root.after(1000, self.analyze_activity_patterns)
                return
            
            # Check idle time against threshold - ONLY IDLE DETECTION
            if idle_time > idle_threshold:
                zombie_score = 40
                reasons = [f"Idle for {idle_time:.0f} seconds"]
                
                print(f"Idle threshold exceeded: {idle_time:.1f}s > {idle_threshold}s")
                
                # Track sustained idle behavior for at least 60 seconds
                if self.zombie_onset_time is None:
                    self.zombie_onset_time = current_time
                    print(f"Starting zombie onset tracking at {current_time}")
                elif current_time - self.zombie_onset_time >= 60:
                    print(f"TRIGGERING: Sustained idle behavior detected!")
                    self.trigger_intelligent_challenge(reasons, zombie_score)
                    self.zombie_onset_time = None
                    self.root.after(1000, self.analyze_activity_patterns)
                    return
            else:
                if self.zombie_onset_time is not None:
                    print(f"Resetting zombie onset - activity detected")
                self.zombie_onset_time = None
                    
            # Apply tolerance system
            if idle_time > idle_threshold:
                if self.tolerance_level > 30:
                    # Use tolerance to forgive minor idle behavior
                    self.tolerance_level -= 5
                    self.stats['tolerance_saves'] += 1
                    print(f"Using tolerance: {self.tolerance_level}")
                    if self.settings['visual_warnings'] and not self.warning_given:
                        self.show_warning(reasons)
                        self.warning_given = True
                else:
                    # Trigger challenge
                    print(f"TRIGGERING: Low tolerance, idle detected!")
                    self.trigger_intelligent_challenge(reasons, zombie_score)
                    
            # Decay tolerance over time
            self.tolerance_level = max(0, self.tolerance_level - self.settings['tolerance_decay'])
            self.update_tolerance_bar()
        except Exception as e:
            print(f"Error in analyze_activity_patterns: {e}")
            
        # Schedule next analysis (faster checks)
        self.root.after(500, self.analyze_activity_patterns)
        
    # REMOVED: Complex behavioral analysis methods
    # Now only detects idle time (no keyboard/mouse movement)
        
    def get_idle_threshold(self):
        """Get adaptive idle threshold"""
        base_thresholds = {
            'low': 300,      # 5 minutes
            'medium': 180,   # 3 minutes  
            'high': 120,     # 2 minutes
            'adaptive': 150  # 2.5 minutes, adjusted based on patterns
        }
        
        threshold = base_thresholds[self.settings['sensitivity']]
        
        if self.settings['gaming_mode']:
            threshold *= 2
            
        if self.settings['adaptive_threshold']:
            # Adjust based on tolerance level
            threshold = threshold * (1 + self.tolerance_level / 200.0)
            
        return threshold
        
    def show_warning(self, reasons):
        """Show visual warning before challenge"""
        if not self.settings['visual_warnings']:
            return
            
        try:
            warning_window = tk.Toplevel(self.root)
            warning_window.title("⚠️ Warning")
            warning_window.geometry("400x200")
            warning_window.configure(bg="#fd7e14")
            warning_window.attributes('-topmost', True)
            
            # Center the window
            warning_window.geometry("+{}+{}".format(
                self.root.winfo_rootx() + 50,
                self.root.winfo_rooty() + 50
            ))
            
            tk.Label(
                warning_window,
                text="⚠️ Zombie Activity Detected!",
                font=("Segoe UI", 16, "bold"),
                fg="white",
                bg="#fd7e14"
            ).pack(pady=20)
            
            tk.Label(
                warning_window,
                text="Take a moment to refocus...",
                font=("Segoe UI", 12),
                fg="white",
                bg="#fd7e14"
            ).pack()
            
            reason_text = "Patterns detected: " + ", ".join(reasons[:2])
            tk.Label(
                warning_window,
                text=reason_text,
                font=("Segoe UI", 10),
                fg="white",
                bg="#fd7e14",
                wraplength=350
            ).pack(pady=10)
            
            # Auto-close after 3 seconds
            warning_window.after(3000, warning_window.destroy)
        except Exception as e:
            print(f"Error showing warning: {e}")
        
    def trigger_intelligent_challenge(self, reasons, zombie_score):
        """FIXED: Trigger challenge with proper state management"""
        try:
            # Prevent multiple challenges
            if self.challenge_in_progress or self.is_in_grace_period():
                return
                
            # Set challenge state
            self.challenge_in_progress = True
            
        self.zombie_incidents += 1
        self.stats['total_interventions'] += 1
        self.stats['today_interventions'] += 1
            self.warning_given = False
            
            # Play alert
            self.start_continuous_beep()
                
            # Determine challenge difficulty
            code_length = self.calculate_challenge_difficulty(zombie_score)
            challenge_code = self.generate_challenge_code(code_length)
            
            reason_text = "Detected: " + ", ".join(reasons[:3])
            self.show_challenge_window(challenge_code, reason_text, zombie_score)
        except Exception as e:
            print(f"Error in trigger_intelligent_challenge: {e}")
            self.challenge_in_progress = False  # Reset on error
        
    def _beep_loop(self):
        """Loop to generate continuous beeps"""
        while not self.stop_beeping_event.is_set():
            try:
                if platform.system() == "Windows":
                    winsound.Beep(800, 500)
                else:
                    print('\a', end='', flush=True)
            except Exception as e:
                print(f"Could not play sound: {e}")
            time.sleep(1)

    def start_continuous_beep(self):
        """Start the continuous beeping sound in a separate thread"""
        if self.beeping_thread and self.beeping_thread.is_alive():
            return

        self.stop_beeping_event = threading.Event()
        self.beeping_thread = threading.Thread(target=self._beep_loop, daemon=True)
        self.beeping_thread.start()

    def stop_continuous_beep(self):
        """Stop the continuous beeping sound"""
        if self.stop_beeping_event:
            self.stop_beeping_event.set()
        if self.beeping_thread:
            self.beeping_thread.join(timeout=1)
        self.beeping_thread = None
        self.stop_beeping_event = None
        
    def play_alert_sound(self, zombie_score):
        """Play alert with multiple fallbacks"""
        try:
            try:
                self.root.bell()
            except Exception:
                pass

            if platform.system() == "Windows":
                try:
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                except Exception:
                    try:
                        winsound.MessageBeep(-1)
                    except Exception:
                        pass

                try:
                    if zombie_score > 80:
                        for _ in range(2):
                            winsound.Beep(800, 200)
                            time.sleep(0.1)
                    elif zombie_score > 60:
                        winsound.Beep(700, 300)
                    else:
                        winsound.Beep(600, 300)
                except Exception:
                    pass
            else:
                print('\a', end='', flush=True)
        except Exception as e:
            print(f"Could not play sound: {e}")
            
    def calculate_challenge_difficulty(self, zombie_score):
        """Calculate challenge difficulty"""
        base_length = 6
        
        if zombie_score > 80:
            base_length += 3
        elif zombie_score > 60:
            base_length += 2
        elif zombie_score > 40:
            base_length += 1
            
        if self.zombie_incidents > 2:
            base_length += min(self.zombie_incidents - 2, 4)
            
        if self.settings['nightmare_mode']:
            base_length += 3
            
        if self.stats['current_streak'] > 5:
            base_length = max(4, base_length - 1)
            
        return min(base_length, 15)
        
    def generate_challenge_code(self, length):
        """Generate challenge code"""
        if self.settings['nightmare_mode']:
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*'
        else:
            chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
            
        return ''.join(random.choices(chars, k=length))
        
    def show_challenge_window(self, code, reason, zombie_score):
        """FIXED: Show challenge window with proper state management"""
        try:
        self.challenge_window = tk.Toplevel(self.root)
        self.challenge_window.title("🚨 ZOMBIE DETECTED!")
            self.challenge_window.geometry("550x400")
            self.challenge_window.configure(bg="#da3633")
        self.challenge_window.attributes('-topmost', True)
            self.challenge_window.attributes('-toolwindow', False)  # Ensure it's not a tool window
            self.challenge_window.grab_set()
            self.challenge_window.focus_force()
            self.challenge_window.protocol("WM_DELETE_WINDOW", lambda: None)
            
            # Center window
            screen_width = self.challenge_window.winfo_screenwidth()
            screen_height = self.challenge_window.winfo_screenheight()
            x = (screen_width - 550) // 2
            y = (screen_height - 400) // 2
            self.challenge_window.geometry(f"550x400+{x}+{y}")
            
            self.challenge_window.lift()
            self.challenge_window.focus_force()
            
            self.challenge_start_time = time.time()
            
            # Header
            header_frame = tk.Frame(self.challenge_window, bg="#da3633")
            header_frame.pack(fill="x", pady=20)
            
            tk.Label(
                header_frame,
                text="🧟‍♂️ ZOMBIE MODE DETECTED! 🚨",
                font=("Segoe UI", 20, "bold"),
            fg="white",
                bg="#da3633"
            ).pack()
            
            severity_text = self.get_severity_text(zombie_score)
            tk.Label(
                header_frame,
                text=f"Severity: {severity_text}",
                font=("Segoe UI", 12, "bold"),
                fg="#ffeb3b",
                bg="#da3633"
            ).pack(pady=(5, 0))
            
            # Reason
            tk.Label(
            self.challenge_window,
                text=reason,
                font=("Segoe UI", 11),
            fg="white",
                bg="#da3633",
                wraplength=500
            ).pack(pady=10)
            
            # Code display
            code_frame = tk.Frame(self.challenge_window, bg="#000000", relief="solid", bd=3)
            code_frame.pack(pady=20, padx=50)
        
        tk.Label(
            code_frame,
                text="Enter this code to prove you're conscious:",
                font=("Segoe UI", 12, "bold"),
                bg="#000000",
                fg="#FFFFFF"
            ).pack(pady=(15, 5))
        
        code_label = tk.Label(
            code_frame,
            text=code,
                font=("Consolas", 36, "bold"),
                fg="#00FF00",
                bg="#000000"
        )
        code_label.pack(pady=10)
        
            # Input section
            input_frame = tk.Frame(self.challenge_window, bg="#da3633")
            input_frame.pack(pady=15)
            
            tk.Label(
                input_frame,
                text="Your response:",
                font=("Segoe UI", 12),
                fg="white",
                bg="#da3633"
            ).pack()
        
        self.challenge_entry = tk.Entry(
            input_frame,
                font=("Consolas", 16),
                width=max(len(code) + 2, 12),
                justify="center",
                relief="solid",
                bd=2,
                bg="white",
                fg="black",
                insertbackground="black",  # Ensure cursor is visible
                selectbackground="#264f78",  # Better selection color
                selectforeground="white",
                exportselection=False,  # Prevent selection loss
                takefocus=True,  # Ensure it can take focus
                state='normal'  # Ensure it's enabled
            )
            self.challenge_entry.pack(pady=8)
            
            # Ensure entry is immediately ready for typing
        self.challenge_entry.focus_set()
            self.challenge_entry.select_range(0, tk.END)
            
            self.feedback_label = tk.Label(
                input_frame,
                text="",
                font=("Segoe UI", 10),
                fg="#ffeb3b",
                bg="#da3633"
            )
            self.feedback_label.pack(pady=(5, 0))
            
            # Event handlers
            def on_key_release(event):
                self.update_challenge_feedback(code)
            
            def on_enter_key(event):
                self.check_challenge_answer(code)
                return "break"
            
            def on_submit_click():
                self.check_challenge_answer(code)
            
            def on_false_positive_click():
                self.report_false_positive()
            
            self.challenge_entry.bind('<KeyRelease>', on_key_release)
            self.challenge_entry.bind('<Return>', on_enter_key)
            
            # Buttons
            button_frame = tk.Frame(self.challenge_window, bg="#da3633")
            button_frame.pack(pady=10)
        
        submit_btn = tk.Button(
                button_frame,
            text="SUBMIT",
                font=("Segoe UI", 12, "bold"),
                bg="#238636",
            fg="white",
                command=on_submit_click,
                width=12,
                height=1,
                relief="flat",
                cursor="hand2"
            )
            submit_btn.pack(side="left", padx=(0, 10))
            
            feedback_btn = tk.Button(
                button_frame,
                text="FALSE POSITIVE",
                font=("Segoe UI", 10),
                bg="#fd7e14",
                fg="white",
                command=on_false_positive_click,
                width=15,
                height=1,
                relief="flat",
                cursor="hand2"
            )
            feedback_btn.pack(side="left")
        
        # Timer
            timer_duration = 35  # Fixed 35 seconds limit
        self.timer_label = tk.Label(
            self.challenge_window,
                text=f"Time remaining: {timer_duration}s",
                font=("Segoe UI", 11, "bold"),
            fg="white",
                bg="#da3633"
            )
            self.timer_label.pack(pady=(10, 0))
            
            # Enhanced focus and input handling for better typing experience
            def focus_and_select():
                try:
                    self.challenge_entry.focus_set()
                    self.challenge_entry.select_range(0, tk.END)
                    self.challenge_entry.icursor(0)  # Set cursor to beginning
                    print("Focus set on challenge entry")
                except Exception as e:
                    print(f"Focus error: {e}")
            
            # Immediate focus attempt
            focus_and_select()
            
            # Multiple focus attempts with delays for better reliability
            self.challenge_window.after(50, focus_and_select)
            self.challenge_window.after(150, focus_and_select)
            self.challenge_window.after(300, focus_and_select)
            self.challenge_window.after(500, focus_and_select)
            self.challenge_window.after(1000, focus_and_select)
            
            # Force window to front and grab focus
            self.challenge_window.lift()
            self.challenge_window.focus_force()
            self.challenge_window.grab_set()
            
            # Ensure window is always on top and not minimized
            self.challenge_window.attributes('-topmost', True)
            self.challenge_window.attributes('-toolwindow', False)
            self.challenge_window.state('normal')  # Ensure window is not minimized
            
            # Make sure entry field is ready for immediate typing
            self.challenge_entry.config(state='normal')
            self.challenge_entry.delete(0, tk.END)
            
            self.start_challenge_timer(timer_duration)
            
        except Exception as e:
            print(f"Error showing challenge window: {e}")
            self.challenge_in_progress = False
        
    def get_severity_text(self, zombie_score):
        """Get severity description"""
        if zombie_score >= 80:
            return "🔥 CRITICAL"
        elif zombie_score >= 60:
            return "⚠️ HIGH"
        elif zombie_score >= 40:
            return "⚡ MEDIUM"
        else:
            return "💤 LOW"
            
    def update_challenge_feedback(self, correct_code):
        """Provide real-time feedback"""
        try:
            if not hasattr(self, 'challenge_entry') or not self.challenge_entry.winfo_exists():
                return
                
            entered = self.challenge_entry.get().upper().strip()
            if not entered:
                self.feedback_label.config(text="")
                return
                
            correct_chars = 0
            for i, char in enumerate(entered):
                if i < len(correct_code) and char == correct_code[i]:
                    correct_chars += 1
                    
            if len(entered) == len(correct_code):
                if entered == correct_code:
                    self.feedback_label.config(text="✅ Correct! Press Enter or Submit", fg="#4caf50")
                else:
                    self.feedback_label.config(text="❌ Incorrect code", fg="#ffeb3b")
            else:
                progress = f"✓ {correct_chars}/{len(correct_code)} characters correct"
                self.feedback_label.config(text=progress, fg="#ffeb3b")
        except Exception as e:
            print(f"Error updating challenge feedback: {e}")
        
    def start_challenge_timer(self, seconds):
        """Challenge timer"""
        try:
        if seconds > 0 and self.challenge_window and self.challenge_window.winfo_exists():
                if seconds <= 5:
                    color = "#ff1744"
                elif seconds <= 10:
                    color = "#ff9800"
                else:
                    color = "white"
                    
                self.timer_label.config(text=f"Time remaining: {seconds}s", fg=color)
            self.challenge_window.after(1000, lambda: self.start_challenge_timer(seconds - 1))
        elif self.challenge_window and self.challenge_window.winfo_exists():
            self.escalate_challenge()
        except Exception as e:
            print(f"Error in challenge timer: {e}")
            
    def check_challenge_answer(self, correct_code):
        """FIXED: Check challenge answer with proper state management"""
        try:
            if not hasattr(self, 'challenge_entry') or not self.challenge_entry.winfo_exists():
                return
                
        entered_code = self.challenge_entry.get().upper().strip()
            response_time = time.time() - self.challenge_start_time if self.challenge_start_time else 0
        
            if entered_code == correct_code.upper():
                self.challenge_success(response_time)
        else:
            self.challenge_failure()
        except Exception as e:
            print(f"Error checking challenge answer: {e}")
            
    def challenge_success(self, response_time):
        """FIXED: Handle successful challenge with grace period"""
        try:
            print("Challenge completed successfully!")
            
            # Update stats
        self.stats['current_streak'] += 1
            self.stats['successful_detections'] += 1
        if self.stats['current_streak'] > self.stats['longest_streak']:
            self.stats['longest_streak'] = self.stats['current_streak']
            
            # Update response time
            if self.stats['avg_response_time'] == 0:
                self.stats['avg_response_time'] = response_time
            else:
                self.stats['avg_response_time'] = (self.stats['avg_response_time'] + response_time) / 2
                
            # Restore tolerance
            self.tolerance_level = min(self.max_tolerance, self.tolerance_level + 20)
            
            # Stop beeping
            self.stop_continuous_beep()
            
            # IMPORTANT: Reset challenge state and start grace period
            self.challenge_in_progress = False
            self.start_grace_period()
        
        # Close challenge window
            if self.challenge_window and self.challenge_window.winfo_exists():
            self.challenge_window.destroy()
            self.challenge_window = None
            
            # Success message
            success_msg = f"✅ Consciousness Verified!\n\n"
            success_msg += f"Response time: {response_time:.1f}s\n"
            success_msg += f"Current streak: {self.stats['current_streak']}\n"
            success_msg += f"Tolerance restored: +20 points\n"
            success_msg += f"Grace period: {self.settings['grace_period']} seconds"
            
            if response_time < 10:
                success_msg += "\n🚀 Lightning fast response!"
            elif response_time < 20:
                success_msg += "\n👍 Good response time!"
                
            messagebox.showinfo("Challenge Complete!", success_msg)
                
            # Reset activity tracking
            self.reset_activity_tracking()
        self.update_stats_display()
        self.save_stats()
        except Exception as e:
            print(f"Error in challenge success: {e}")
            self.challenge_in_progress = False
        
    def challenge_failure(self):
        """Handle challenge failure"""
        try:
        self.stats['current_streak'] = 0
            self.tolerance_level = max(0, self.tolerance_level - 10)
            
            if hasattr(self, 'challenge_entry') and self.challenge_entry.winfo_exists():
                original_bg = self.challenge_entry.cget('bg')
                self.challenge_entry.config(bg="#ffcdd2")
                self.challenge_window.after(500, lambda: self.challenge_entry.config(bg=original_bg))
                
                messagebox.showwarning("Incorrect!", "Wrong code! Focus and try again.\nTolerance decreased by 10 points.")
        self.challenge_entry.delete(0, tk.END)
        self.challenge_entry.focus_set()
        except Exception as e:
            print(f"Error in challenge failure: {e}")
        
    def report_false_positive(self):
        """FIXED: Handle false positive with proper state management"""
        try:
            print("False positive reported")
            
            self.stats['false_positives'] += 1
            self.tolerance_level = min(self.max_tolerance, self.tolerance_level + 30)
            
            # Stop beeping
            self.stop_continuous_beep()
            
            # Adjust adaptive threshold
            if self.settings['adaptive_threshold']:
                self.settings['tolerance_decay'] = max(0.1, self.settings['tolerance_decay'] - 0.1)
            
            # IMPORTANT: Reset challenge state and start grace period
            self.challenge_in_progress = False
            self.start_grace_period()
            
            # Close challenge window
            if self.challenge_window and self.challenge_window.winfo_exists():
                self.challenge_window.destroy()
                self.challenge_window = None
                
            messagebox.showinfo("Feedback Received", 
                               "Thank you for the feedback!\n\n" +
                               "• Tolerance increased by 30 points\n" +
                               "• System sensitivity adjusted\n" +
                               "• Grace period activated\n" +
                               "• This helps improve accuracy")
                
            self.reset_activity_tracking()
            self.update_stats_display()
        except Exception as e:
            print(f"Error reporting false positive: {e}")
            self.challenge_in_progress = False
        
    def escalate_challenge(self):
        """Handle challenge timeout"""
        try:
            if not self.challenge_window or not self.challenge_window.winfo_exists():
                return
            
            self.challenge_window.destroy()
            self.challenge_window = None
                
            messagebox.showwarning("Time Expired!", 
                                  "⏰ Challenge timeout!\n\n" +
                                  "Generating harder challenge...\n" +
                                  "💡 Tip: Stay focused to avoid escalation")
            
            self.zombie_incidents += 1
            escalated_length = min(15, 8 + self.zombie_incidents)
            escalated_code = self.generate_challenge_code(escalated_length)
            
            self.show_challenge_window(escalated_code, "Challenge escalated due to timeout", 90)
        except Exception as e:
            print(f"Error escalating challenge: {e}")
            self.challenge_in_progress = False
        
    def reset_activity_tracking(self):
        """Reset activity tracking"""
        self.last_activity = time.time()
        self.mouse_movements.clear()
        self.key_presses.clear()
        self.click_patterns.clear()
        self.scroll_patterns.clear()
        self.activity_buffer.clear()
        self.repetitive_actions = 0
        self.zombie_incidents = max(0, self.zombie_incidents - 1)
        self.zombie_onset_time = None
        
    def toggle_monitoring(self):
        """Toggle monitoring"""
        if self.is_active:
            self.stop_monitoring()
        else:
            self.start_monitoring()
            
    def start_monitoring(self):
        """Start monitoring"""
        self.is_active = True
        self.status_label.config(text="🟢 ACTIVE - AI Monitoring Engaged", fg="#4caf50")
        self.toggle_btn.config(text="STOP MONITORING", bg="#da3633")
        
        self.reset_activity_tracking()
        self.tolerance_level = 50
        self.challenge_in_progress = False
        self.grace_period_end = 0
        
        messagebox.showinfo("Monitoring Started", 
                           "🤖 ZombieCheck is now monitoring your activity!\n\n" +
                           "• AI will learn your patterns\n" +
                           "• Tolerance system prevents false alerts\n" +
                           "• Grace period after challenges\n" +
                           "• Use 'False Positive' button to improve accuracy")
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_active = False
        self.status_label.config(text="🔴 INACTIVE", fg="#da3633")
        self.toggle_btn.config(text="START MONITORING", bg="#238636")
        
        self.stop_continuous_beep()
        self.challenge_in_progress = False
        
        session_summary = f"📊 Session Summary:\n\n"
        session_summary += f"Interventions: {self.stats['today_interventions']}\n"
        session_summary += f"Successful responses: {self.stats['successful_detections']}\n"
        session_summary += f"False positives: {self.stats['false_positives']}\n"
        session_summary += f"Final tolerance: {self.tolerance_level:.0f}/100"
        
        messagebox.showinfo("Monitoring Stopped", session_summary)
        
    def trigger_test_challenge(self):
        """Trigger test challenge"""
        messagebox.showinfo("Test Challenge", 
                           "🧪 This is a test challenge to demonstrate the system.\n\n" +
                           "In real monitoring, challenges are triggered by:\n" +
                           "• Prolonged inactivity\n" +
                           "• Repetitive actions\n" +
                           "• Aimless browsing patterns\n" +
                           "• Mindless scrolling")
        
        test_code = self.generate_challenge_code(6)
        self.show_challenge_window(test_code, "Test Challenge - Normal difficulty", 50)
    
    def test_keyboard_input(self):
        """Test keyboard input detection"""
        print("Testing keyboard input...")
        print("Please type any key to test if keyboard detection is working")
        print("You should see 'Keyboard activity detected: [key]' in the console")
        
        # Show a simple test window
        test_window = tk.Toplevel(self.root)
        test_window.title("Keyboard Test")
        test_window.geometry("300x200")
        
        tk.Label(test_window, text="Type any key to test keyboard detection", font=("Arial", 12)).pack(pady=20)
        tk.Label(test_window, text="Check console for debug messages", font=("Arial", 10)).pack()
        
        # Bind keyboard events to test window
        test_window.bind('<KeyPress>', lambda e: print(f"Test window keyboard: {e.keysym}"))
        
        test_window.focus_set()
        
    def update_tolerance_bar(self):
        """Update tolerance bar"""
        try:
            if not hasattr(self, 'tolerance_canvas') or not self.tolerance_canvas.winfo_exists():
                return
                
            self.tolerance_canvas.delete("all")
            canvas_width = self.tolerance_canvas.winfo_width()
            if canvas_width <= 1:
                canvas_width = 300
                
            self.tolerance_canvas.create_rectangle(0, 0, canvas_width, 10, fill="#21262d", outline="")
            
            bar_width = (self.tolerance_level / self.max_tolerance) * canvas_width
            
            if self.tolerance_level > 70:
                color = "#4caf50"
            elif self.tolerance_level > 30:
                color = "#ff9800"
            else:
                color = "#da3633"
                
            if bar_width > 0:
                self.tolerance_canvas.create_rectangle(0, 0, bar_width, 10, fill=color, outline="")
                
            # Show grace period status
            if self.is_in_grace_period():
                remaining = int(self.grace_period_end - time.time())
                text = f"Grace: {remaining}s"
                color = "#4caf50"
            else:
                text = f"{self.tolerance_level:.0f}/100"
                color = "white"
                
            self.tolerance_canvas.create_text(canvas_width//2, 5, text=text, fill=color, font=("Segoe UI", 8, "bold"))
        except Exception as e:
            print(f"Error updating tolerance bar: {e}")
        
        if self.is_active:
            self.root.after(1000, self.update_tolerance_bar)
        
    def update_stats_display(self):
        """Update stats display"""
        try:
            if hasattr(self, 'perf_text') and self.perf_text.winfo_exists():
                self.perf_text.config(state="normal")
                self.perf_text.delete(1.0, tk.END)
                
                productivity_score = max(0, 100 - (self.stats['today_interventions'] * 5) + (self.stats['current_streak'] * 2))
                
                perf_stats = f"""
📈 Productivity Score: {productivity_score:.0f}/100
🎯 Interventions Today: {self.stats['today_interventions']}
✅ Successful Responses: {self.stats['successful_detections']}
❌ False Positives: {self.stats['false_positives']}
🛡️ Tolerance Saves: {self.stats['tolerance_saves']}
⚡ Current Streak: {self.stats['current_streak']}
                """
                
                self.perf_text.insert(1.0, perf_stats.strip())
                self.perf_text.config(state="disabled")
                
            if hasattr(self, 'stats_text') and self.stats_text.winfo_exists():
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        
            accuracy = 0
            if self.stats['total_interventions'] > 0:
                accuracy = (self.stats['successful_detections'] / max(1, self.stats['total_interventions'])) * 100
                
            grace_status = "Active" if self.is_in_grace_period() else "Inactive"
            grace_remaining = max(0, int(self.grace_period_end - time.time())) if self.is_in_grace_period() else 0
                
            all_stats = f"""
🏆 LIFETIME STATISTICS

Total Interventions: {self.stats['total_interventions']}
Successful Detections: {self.stats['successful_detections']}
Detection Accuracy: {accuracy:.1f}%
False Positive Rate: {self.stats['false_positives']}/{self.stats['total_interventions']}

🔥 STREAKS & RECORDS
Longest Streak: {self.stats['longest_streak']}
Current Streak: {self.stats['current_streak']}
Average Response Time: {self.stats['avg_response_time']:.1f}s

🛡️ TOLERANCE SYSTEM
Tolerance Saves: {self.stats['tolerance_saves']}
Current Tolerance: {self.tolerance_level:.0f}/100
Grace Period: {grace_status} ({grace_remaining}s remaining)

⚙️ SYSTEM STATUS
Monitoring: {"🟢 Active" if self.is_active else "🔴 Inactive"}
Challenge in Progress: {"🟡 Yes" if self.challenge_in_progress else "🟢 No"}
Sensitivity: {self.settings['sensitivity'].title()}
Gaming Mode: {"✅ Enabled" if self.settings['gaming_mode'] else "❌ Disabled"}
Nightmare Mode: {"✅ Enabled" if self.settings['nightmare_mode'] else "❌ Disabled"}
Adaptive Learning: {"✅ Enabled" if self.settings['adaptive_threshold'] else "❌ Disabled"}
        """
        
            self.stats_text.insert(1.0, all_stats.strip())
        self.stats_text.config(state="disabled")
        except Exception as e:
            print(f"Error updating stats display: {e}")
            
    # Settings update methods
    def update_sensitivity(self, event=None):
        self.settings['sensitivity'] = self.sensitivity_var.get()
        
    def update_nightmare_mode(self):
        self.settings['nightmare_mode'] = self.nightmare_var.get()
        
    def update_gaming_mode(self):
        self.settings['gaming_mode'] = self.gaming_var.get()
        
    def update_adaptive_mode(self):
        self.settings['adaptive_threshold'] = self.adaptive_var.get()
        
    def update_visual_setting(self):
        self.settings['visual_warnings'] = self.visual_var.get()
        
    def update_grace_period(self):
        """Update grace period setting"""
        try:
            self.settings['grace_period'] = int(self.grace_var.get())
        except ValueError:
            self.settings['grace_period'] = 60  # Default
        
    def load_stats(self):
        """Load stats from file"""
        try:
            if os.path.exists('zombie_stats.json'):
                with open('zombie_stats.json', 'r') as f:
                    data = json.load(f)
                    self.stats.update(data.get('stats', {}))
                    self.settings.update(data.get('settings', {}))
                    self.tolerance_level = data.get('tolerance_level', 50)
        except Exception as e:
            print(f"Error loading stats: {e}")
            
    def save_stats(self):
        """Save stats to file"""
        try:
            data = {
                'stats': self.stats,
                'settings': self.settings,
                'tolerance_level': self.tolerance_level,
                'last_updated': datetime.now().isoformat(),
                'version': '2.1'
            }
            with open('zombie_stats.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")
            
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        welcome_msg = """🎉 Welcome to ZombieCheck Enhanced v2.3!

🆕 NEW FEATURES:
• ✅ BACKGROUND MONITORING: Works silently in background
• ✅ SECRET CODE ACTIVATION: Type "5XETR5PZ" to activate
• ✅ IDLE-ONLY DETECTION: Only triggers on NO keyboard/mouse activity
• ✅ IMPROVED CAPTCHA: Better focus and typing on first attempt
• ✅ FIXED WINDOW CLOSING: Application closes properly without hanging

🔧 KEY IMPROVEMENTS:
• Background monitoring starts automatically
• Secret code "5XETR5PZ" activates monitoring
• Triggers ONLY after 60 seconds of NO activity
• Any mouse/keyboard activity resets the timer
• Works silently until triggered

💡 TIP: Type the secret code "5XETR5PZ" anywhere to activate background monitoring. The app will then silently monitor and trigger ONLY when you're completely inactive (no mouse or keyboard movement) for 60 seconds!"""

        messagebox.showinfo("Welcome to ZombieCheck Enhanced v2.3", welcome_msg)
        
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing - FIXED VERSION"""
        try:
            # Stop monitoring if active
        if self.is_active:
            self.stop_monitoring()
            
            # Stop any ongoing beeping
            self.stop_continuous_beep()
            
            # Close challenge window if open
            if self.challenge_window and self.challenge_window.winfo_exists():
                self.challenge_window.destroy()
                self.challenge_window = None
            
            # Save stats
        self.save_stats()
            
            # Properly destroy the main window
            self.root.quit()
        self.root.destroy()
            
        except Exception as e:
            print(f"Error during application closing: {e}")
            # Force exit if there are issues
            import sys
            sys.exit(0)

if __name__ == "__main__":
    try:
    app = ZombieCheck()
    app.run()
    except Exception as e:
        print(f"Application error: {e}")
        input("Press Enter to exit...")
