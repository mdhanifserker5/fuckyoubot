#!/usr/bin/env python3
"""
🤖 Professional VPN Selling Bot - With Activation Code Support
"""

import os
import json
import logging
import datetime
import asyncio
from typing import List, Tuple, Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler
)

# ==================== CONFIGURATION ====================
BOT_TOKEN = "7976259085:AAGs6LYjre1l20ShUT7wkwtyjESVki_lAAM"
ADMIN_ID = 6986785327
SUPPORT_USERNAME = "@HANIF11ss"

# VPN Prices
VPN_PRICE_TAKA = 50
VPN_PRICE_USD = 0.4

# File paths
VPN_FOLDER = "vpn-stock"
NORD_FILE = os.path.join(VPN_FOLDER, "nord.txt")
SURFSHARK_FILE = os.path.join(VPN_FOLDER, "surfshark.txt")
CYBERGHOST_FILE = os.path.join(VPN_FOLDER, "cyberghost.txt")
EXPRESSVPN_FILE = os.path.join(VPN_FOLDER, "expressvpn.txt")
HMA_FILE = os.path.join(VPN_FOLDER, "hma.txt")
PROTON_FILE = os.path.join(VPN_FOLDER, "proton.txt")
IPVANISH_FILE = os.path.join(VPN_FOLDER, "ipvanish.txt")
VYPER_FILE = os.path.join(VPN_FOLDER, "vyper.txt")
PANDA_FILE = os.path.join(VPN_FOLDER, "panda.txt")
HOTSPOT_FILE = os.path.join(VPN_FOLDER, "hotspot.txt")
NORTON_FILE = os.path.join(VPN_FOLDER, "norton.txt")  

# State tracking
(
    MAIN_MENU,
    VPN_MENU,
    QUANTITY_SELECTION,
    PAYMENT_INFO,
    ADMIN_MENU,
    ADD_BALANCE_MENU,
    VIEW_STOCK,
    ADD_VPN_MENU
) = range(8)

# ==================== SETUP LOGGING ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== VPN FILE MANAGER ====================
class VPNFileManager:
    @staticmethod
    def get_vpn_count(vpn_type: str) -> int:
        """Get available VPN count from file"""
        file_map = {
            'nord': NORD_FILE,
            'surfshark': SURFSHARK_FILE,
            'cyberghost': CYBERGHOST_FILE,
            'expressvpn': EXPRESSVPN_FILE,
            'hma': HMA_FILE,
            'proton': PROTON_FILE,
            'ipvanish': IPVANISH_FILE,
            'vyper': VYPER_FILE,
            'panda': PANDA_FILE,
            'hotspot': HOTSPOT_FILE,
            'norton': NORTON_FILE  
        }
        
        file_path = file_map.get(vpn_type)
        if not file_path or not os.path.exists(file_path):
            return 0
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                return len(lines)
        except:
            return 0
    
    @staticmethod
    def get_vpn_account(vpn_type: str, quantity: int = 1) -> List[str]:
        """Get VPN accounts from file"""
        file_map = {
            'nord': NORD_FILE,
            'surfshark': SURFSHARK_FILE,
            'cyberghost': CYBERGHOST_FILE,
            'expressvpn': EXPRESSVPN_FILE,
            'hma': HMA_FILE,
            'proton': PROTON_FILE,
            'ipvanish': IPVANISH_FILE,
            'vyper': VYPER_FILE,
            'panda': PANDA_FILE,
            'hotspot': HOTSPOT_FILE,
            'norton': NORTON_FILE  
        }
        
        file_path = file_map.get(vpn_type)
        if not file_path or not os.path.exists(file_path):
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                all_lines = [line.strip() for line in f if line.strip()]
                
            if quantity > len(all_lines):
                quantity = len(all_lines)
                
            # Get first 'quantity' accounts
            accounts = all_lines[:quantity]
            
            # Remove used accounts from file
            remaining = all_lines[quantity:]
            with open(file_path, 'w', encoding='utf-8') as f:
                for line in remaining:
                    f.write(line + '\n')
                    
            return accounts
        except Exception as e:
            logger.error(f"Error reading VPN file: {e}")
            return []
    
    @staticmethod
    def add_vpn_account(vpn_type: str, accounts: List[str]) -> bool:
        """Add new VPN accounts to file"""
        file_map = {
            'nord': NORD_FILE,
            'surfshark': SURFSHARK_FILE,
            'cyberghost': CYBERGHOST_FILE,
            'expressvpn': EXPRESSVPN_FILE,
            'hma': HMA_FILE,
            'proton': PROTON_FILE,
            'ipvanish': IPVANISH_FILE,
            'vyper': VYPER_FILE,
            'panda': PANDA_FILE,
            'hotspot': HOTSPOT_FILE,
            'norton': NORTON_FILE 
        }
        
        file_path = file_map.get(vpn_type)
        if not file_path:
            return False
            
        try:
            # Create folder if not exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'a', encoding='utf-8') as f:
                for account in accounts:
                    if account.strip():
                        f.write(account.strip() + '\n')
            return True
        except Exception as e:
            logger.error(f"Error adding VPN account: {e}")
            return False
    
    @staticmethod
    def view_all_vpn() -> str:
        """View all VPN stock"""
        result = "📊 *VPN Stock Status:*\n\n"
        
        vpn_types = [
            ('nord', '🔰 NordVPN'),
            ('surfshark', '🦈 Surfshark VPN'),
            ('cyberghost', '👻 CyberGhost VPN'),
            ('expressvpn', '⚡ ExpressVPN'),
            ('hma', '🏴󠁧󠁢󠁥󠁮󠁧󠁿 HMA VPN'),
            ('proton', '🔐 Proton VPN'),
            ('ipvanish', '🌀 IPVanish VPN'),
            ('vyper', '🐍 Vyper VPN'),
            ('panda', '🐼 Panda VPN'),
            ('hotspot', '🛡️ Hotspot Shield VPN'),
            ('norton', '🛡️ Norton VPN')  
        ]
        
        for vpn_type, name in vpn_types:
            count = VPNFileManager.get_vpn_count(vpn_type)
            result += f"• *{name}:* {count} accounts\n"
            
        return result

# ==================== USER BALANCE MANAGER ====================
class BalanceManager:
    def __init__(self):
        self.balance_file = "user_balance.json"
    
    def get_balance(self, user_id: int) -> int:
        """Get user balance"""
        try:
            if os.path.exists(self.balance_file):
                with open(self.balance_file, 'r') as f:
                    balances = json.load(f)
                    return balances.get(str(user_id), 0)
            return 0
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0
    
    def set_balance(self, user_id: int, amount: int) -> bool:
        """Set user balance (for admin)"""
        try:
            # Load existing balances
            if os.path.exists(self.balance_file):
                with open(self.balance_file, 'r') as f:
                    balances = json.load(f)
            else:
                balances = {}
            
            # Update balance
            balances[str(user_id)] = amount
            
            # Save
            with open(self.balance_file, 'w') as f:
                json.dump(balances, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Error setting balance: {e}")
            return False
    
    def add_balance(self, user_id: int, amount: int) -> Tuple[bool, int]:
        """Add balance to user"""
        try:
            current = self.get_balance(user_id)
            new_balance = current + amount
            
            # Save new balance
            self.set_balance(user_id, new_balance)
            
            return True, new_balance
        except Exception as e:
            logger.error(f"Error adding balance: {e}")
            return False, 0
    
    def deduct_balance(self, user_id: int, amount: int) -> Tuple[bool, int]:
        """Deduct balance from user"""
        current = self.get_balance(user_id)
        
        if current < amount:
            return False, current  # Insufficient balance
        
        new_balance = current - amount
        success = self.set_balance(user_id, new_balance)
        
        return success, new_balance

# ==================== KEYBOARD CREATION ====================
def create_main_keyboard() -> InlineKeyboardMarkup:
    """Create main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🛒 Buy VPN", callback_data='buy_vpn'),
         InlineKeyboardButton("💰 My Balance", callback_data='my_balance')],
        [InlineKeyboardButton("📋 My Orders", callback_data='my_orders'),
         InlineKeyboardButton("📞 Support", url=f'https://t.me/{SUPPORT_USERNAME.replace("@", "")}')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help'),
         InlineKeyboardButton("⚡ Admin", callback_data='admin_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_vpn_keyboard() -> InlineKeyboardMarkup:
    """Create VPN selection keyboard with 2 columns"""
    keyboard = [
        # Row 1
        [InlineKeyboardButton("🔰 NordVPN", callback_data='select_nord'),
         InlineKeyboardButton("🦈 Surfshark", callback_data='select_surfshark')],
        # Row 2
        [InlineKeyboardButton("👻 CyberGhost", callback_data='select_cyberghost'),
         InlineKeyboardButton("⚡ ExpressVPN", callback_data='select_expressvpn')],
        # Row 3
        [InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 HMA VPN", callback_data='select_hma'),
         InlineKeyboardButton("🔐 Proton VPN", callback_data='select_proton')],
        # Row 4
        [InlineKeyboardButton("🌀 IPVanish", callback_data='select_ipvanish'),
         InlineKeyboardButton("🐍 Vyper VPN", callback_data='select_vyper')],
        # Row 5
        [InlineKeyboardButton("🐼 Panda VPN", callback_data='select_panda'),
         InlineKeyboardButton("🛡️ Hotspot Shield", callback_data='select_hotspot')],
        # Row 6 - ADDED Norton VPN
        [InlineKeyboardButton("🛡️ Norton VPN", callback_data='select_norton')],
        # Back button
        [InlineKeyboardButton("↩️ Back to Main", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_quantity_keyboard(vpn_type: str) -> InlineKeyboardMarkup:
    """Create quantity selection keyboard (1-10)"""
    keyboard = []
    
    # Create rows for quantity buttons
    row1, row2 = [], []
    for i in range(1, 6):
        row1.append(InlineKeyboardButton(str(i), callback_data=f'qty_{vpn_type}_{i}'))
    for i in range(6, 11):
        row2.append(InlineKeyboardButton(str(i), callback_data=f'qty_{vpn_type}_{i}'))
    
    keyboard.append(row1)
    keyboard.append(row2)
    keyboard.append([InlineKeyboardButton("↩️ Back to VPN List", callback_data='buy_vpn')])
    
    return InlineKeyboardMarkup(keyboard)

def create_payment_info_keyboard() -> InlineKeyboardMarkup:
    """Create payment information keyboard"""
    keyboard = [
        [InlineKeyboardButton("📞 Contact for Payment", url=f'https://t.me/{SUPPORT_USERNAME.replace("@", "")}')],
        [InlineKeyboardButton("💰 Check Balance", callback_data='my_balance'),
         InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_admin_keyboard() -> InlineKeyboardMarkup:
    """Create admin panel keyboard"""
    keyboard = [
        [InlineKeyboardButton("👤 Add User Balance", callback_data='admin_add_balance'),
         InlineKeyboardButton("📊 View VPN Stock", callback_data='admin_view_stock')],
        [InlineKeyboardButton("➕ Add VPN Stock", callback_data='admin_add_vpn'),
         InlineKeyboardButton("📈 User Statistics", callback_data='admin_stats')],
        [InlineKeyboardButton("🔙 Back to Main", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_back_keyboard(back_to: str = 'main_menu') -> InlineKeyboardMarkup:
    """Create simple back button keyboard"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=back_to)]]
    return InlineKeyboardMarkup(keyboard)

# ==================== MESSAGE TEXTS ====================
def get_welcome_text(user) -> str:
    """Get welcome message text"""
    return f"""
🎉 *Welcome to VPN Store, {user.first_name}!* 🎉

🤖 *Professional VPN Selling Bot*

*🌟 Available VPN Services:*
• 🔰 NordVPN - 7 Days
• 🦈 Surfshark VPN - 7 Days  
• 👻 CyberGhost VPN - 7 Days
• ⚡ ExpressVPN - 7 Days
• 🏴󠁧󠁢󠁥󠁮󠁧󠁿 HMA VPN - 7 Days
• 🔐 Proton VPN - 7 Days
• 🌀 IPVanish VPN - 7 Days
• 🐍 Vyper VPN - 7 Days
• 🐼 Panda VPN - 7 Days
• 🛡️ Hotspot Shield VPN - 7 Days
• 🛡️ Norton VPN - 7 Days 

*💰 Price:* ৳{VPN_PRICE_TAKA} per VPN | ${VPN_PRICE_USD}
*🔢 Buy 1 to 10 VPNs at once*
*⏰ Duration:* 7 Days for all VPNs

*📞 Support:* {SUPPORT_USERNAME}
*🆔 Your ID:* `{user.id}`

*Select an option below:*
"""

def get_vpn_menu_text() -> str:
    """Get VPN menu text"""
    vpn_manager = VPNFileManager()
    
    nord_count = vpn_manager.get_vpn_count('nord')
    surf_count = vpn_manager.get_vpn_count('surfshark')
    ghost_count = vpn_manager.get_vpn_count('cyberghost')
    express_count = vpn_manager.get_vpn_count('expressvpn')
    hma_count = vpn_manager.get_vpn_count('hma')
    proton_count = vpn_manager.get_vpn_count('proton')
    ipvanish_count = vpn_manager.get_vpn_count('ipvanish')
    vyper_count = vpn_manager.get_vpn_count('vyper')
    panda_count = vpn_manager.get_vpn_count('panda')
    hotspot_count = vpn_manager.get_vpn_count('hotspot')
    norton_count = vpn_manager.get_vpn_count('norton') 
    
    return f"""
🛒 *Buy VPN Service*

*📊 Available VPN Stock:*
• 🔰 *NordVPN:* {nord_count} accounts
• 🦈 *Surfshark VPN:* {surf_count} accounts  
• 👻 *CyberGhost VPN:* {ghost_count} accounts
• ⚡ *ExpressVPN:* {express_count} accounts
• 🏴󠁧󠁢󠁥󠁮󠁧󠁿 *HMA VPN:* {hma_count} accounts
• 🔐 *Proton VPN:* {proton_count} accounts
• 🌀 *IPVanish VPN:* {ipvanish_count} accounts
• 🐍 *Vyper VPN:* {vyper_count} accounts
• 🐼 *Panda VPN:* {panda_count} accounts
• 🛡️ *Hotspot Shield:* {hotspot_count} accounts
• 🛡️ *Norton VPN:* {norton_count} accounts 

*💰 Price:* ৳{VPN_PRICE_TAKA} per VPN
*⏰ Duration:* 7 Days
*🔢 Max:* 10 VPNs per order

*Select VPN type:*
"""

def get_balance_text(user_id: int, balance_manager: BalanceManager) -> str:
    """Get user balance text"""
    balance = balance_manager.get_balance(user_id)
    
    return f"""
💰 *Your Account Balance*

*Current Balance:* ৳{balance}
*In USD:* ${round(balance * 0.008, 2)}

*💡 Balance Information:*
• 1 VPN = ৳{VPN_PRICE_TAKA}
• You can buy: {balance // VPN_PRICE_TAKA} VPN(s)

*📝 To Add Balance:*
1. Send payment to:
   • Nagad/Bkash/Rocket: `+8801985110052`
   • Binance ID: `1139934779`
   • USDT (BSC): `0xca0b6e096126ccbf5780bc6d65772ad6395d1fe6`
2. Contact {SUPPORT_USERNAME}
3. Provide your User ID: `{user_id}`
4. Wait for confirmation

*📞 Support:* {SUPPORT_USERNAME}
"""

def get_payment_info_text(user_id: int) -> str:
    """Get payment information text"""
    return f"""
💰 *Payment Information*

*💳 Payment Methods:*

📱 *Nagad / bKash / Rocket*
• Number: `+8801985110052`
• Send money and save transaction ID

🌐 *Binance*
• ID: `1139934779`
• Send USDT (BEP20)

₿ *USDT (BSC)*
• Address: `0xca0b6e096126ccbf5780bc6d65772ad6395d1fe6`
• Network: BSC (BEP20)

*📝 After Payment:*
1. Contact {SUPPORT_USERNAME}
2. Provide:
   • Your User ID: `{user_id}`
   • Amount sent
   • Transaction ID/Proof
3. Wait for confirmation (5-30 mins)

*Minimum Deposit:* ৳250 / $2
*🆔 Your User ID:* `{user_id}`
"""

def get_help_text() -> str:
    """Get help text"""
    return f"""
❓ *Help & Support Center*

*📞 Contact Support:*
• Telegram: {SUPPORT_USERNAME}
• Response Time: < 1 hour
• 24/7 Support Available

*🔧 Frequently Asked Questions:*

*Q: How to setup VPN?*
A: Download official VPN app, enter username & password.

*Q: VPN not working?*
A: 1. Check credentials 2. Try different server 3. Contact support.

*Q: Payment not confirmed?*
A: Send transaction ID to {SUPPORT_USERNAME}.

*Q: How long VPN valid?*
A: 7 days from activation.

*Q: Can I get refund?*
A: Refund within 24 hours if VPN not working.

*🛠️ Quick Solutions:*
• Setup help → Ask for guide
• Payment issue → Send transaction proof
• Account problem → Provide User ID
• VPN expired → Buy new subscription
"""

# ==================== BOT HANDLERS ====================
class VPNBot:
    def __init__(self):
        self.vpn_manager = VPNFileManager()
        self.balance_manager = BalanceManager()
        self.application = None
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user = update.effective_user
        
        # Check if user is admin
        if user.id == ADMIN_ID:
            logger.info(f"Admin {user.id} ({user.username}) started the bot")
        
        await update.message.reply_text(
            get_welcome_text(user),
            reply_markup=create_main_keyboard(),
            parse_mode='Markdown'
        )
        return MAIN_MENU
    
    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle main menu callback"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            get_welcome_text(query.from_user),
            reply_markup=create_main_keyboard(),
            parse_mode='Markdown'
        )
        return MAIN_MENU
    
    async def buy_vpn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle buy VPN callback"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            get_vpn_menu_text(),
            reply_markup=create_vpn_keyboard(),
            parse_mode='Markdown'
        )
        return VPN_MENU
    
    async def select_vpn_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle VPN type selection"""
        query = update.callback_query
        await query.answer()
        
        # Extract VPN type from callback data
        # Format: select_nord -> nord
        vpn_type = query.data.replace('select_', '')
        
        # Store in context for later use
        context.user_data['selected_vpn'] = vpn_type
        
        # Check stock
        available = self.vpn_manager.get_vpn_count(vpn_type)
        
        if available <= 0:
            vpn_names = {
                'nord': 'NordVPN',
                'surfshark': 'Surfshark VPN',
                'cyberghost': 'CyberGhost VPN',
                'expressvpn': 'ExpressVPN',
                'hma': 'HMA VPN',
                'proton': 'Proton VPN',
                'ipvanish': 'IPVanish VPN',
                'vyper': 'Vyper VPN',
                'panda': 'Panda VPN',
                'hotspot': 'Hotspot Shield VPN',
                'norton': 'Norton VPN'  
            }
            vpn_name = vpn_names.get(vpn_type, vpn_type)
            
            await query.edit_message_text(
                f"⚠️ *{vpn_name} Out of Stock!*\n\n"
                f"Sorry, {vpn_name} is currently unavailable.\n"
                f"Please check other VPN options or contact support.\n\n"
                f"📞 {SUPPORT_USERNAME}",
                reply_markup=create_vpn_keyboard(),
                parse_mode='Markdown'
            )
            return VPN_MENU
        
        # Show quantity selection
        vpn_names = {
            'nord': 'NordVPN',
            'surfshark': 'Surfshark VPN',
            'cyberghost': 'CyberGhost VPN',
            'expressvpn': 'ExpressVPN',
            'hma': 'HMA VPN',
            'proton': 'Proton VPN',
            'ipvanish': 'IPVanish VPN',
            'vyper': 'Vyper VPN',
            'panda': 'Panda VPN',
            'hotspot': 'Hotspot Shield VPN',
            'norton': 'Norton VPN' 
        }
        vpn_name = vpn_names.get(vpn_type, vpn_type)
        
        quantity_text = f"""
✅ *{vpn_name} Selected*

*Available Stock:* {available} accounts
*Price per VPN:* ৳{VPN_PRICE_TAKA}
*Max purchase:* {min(10, available)} VPNs

*How many VPNs do you want to buy?*
(Select quantity 1-10)
        """
        
        await query.edit_message_text(
            quantity_text,
            reply_markup=create_quantity_keyboard(vpn_type),
            parse_mode='Markdown'
        )
        return QUANTITY_SELECTION
    
    async def select_quantity(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle quantity selection"""
        query = update.callback_query
        await query.answer()
        
        # Parse callback data: qty_nord_3
        parts = query.data.split('_')
        if len(parts) != 3:
            await query.edit_message_text(
                "Error processing request. Please try again.",
                reply_markup=create_main_keyboard()
            )
            return MAIN_MENU
        
        vpn_type = parts[1]
        quantity = int(parts[2])
        
        # Get available stock
        available = self.vpn_manager.get_vpn_count(vpn_type)
        
        if quantity > available:
            await query.answer(f"⚠️ Only {available} accounts available!", show_alert=True)
            return QUANTITY_SELECTION
        
        # Calculate total price
        total_price = quantity * VPN_PRICE_TAKA
        
        # Get user balance
        user_id = query.from_user.id
        user_balance = self.balance_manager.get_balance(user_id)
        
        vpn_names = {
            'nord': 'NordVPN',
            'surfshark': 'Surfshark VPN',
            'cyberghost': 'CyberGhost VPN',
            'expressvpn': 'ExpressVPN',
            'hma': 'HMA VPN',
            'proton': 'Proton VPN',
            'ipvanish': 'IPVanish VPN',
            'vyper': 'Vyper VPN',
            'panda': 'Panda VPN',
            'hotspot': 'Hotspot Shield VPN',
            'norton': 'Norton VPN' 
        }
        vpn_name = vpn_names.get(vpn_type, vpn_type)
        
        if user_balance < total_price:
            # Insufficient balance
            needed = total_price - user_balance
            
            insufficient_text = f"""
⚠️ *Insufficient Balance!*

*Order Details:*
• VPN: {vpn_name}
• Quantity: {quantity}
• Price per VPN: ৳{VPN_PRICE_TAKA}
• Total Price: ৳{total_price}
• Your Balance: ৳{user_balance}

*You need ৳{needed} more.*

Please add balance first:
            """
            
            keyboard = [
                [InlineKeyboardButton("💰 How to Add Balance", callback_data='payment_info')],
                [InlineKeyboardButton("🔙 Change Quantity", callback_data=f'select_{vpn_type}'),
                 InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
            
            await query.edit_message_text(
                insufficient_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            return PAYMENT_INFO
        
        # Process purchase
        order_id = f"VPN{user_id}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Get VPN accounts from file
        vpn_accounts = self.vpn_manager.get_vpn_account(vpn_type, quantity)
        
        if not vpn_accounts or len(vpn_accounts) < quantity:
            await query.edit_message_text(
                "❌ Error: Unable to get VPN accounts. Please try again or contact support.",
                reply_markup=create_main_keyboard(),
                parse_mode='Markdown'
            )
            return MAIN_MENU
        
        # Deduct balance
        success, new_balance = self.balance_manager.deduct_balance(user_id, total_price)
        
        if not success:
            await query.edit_message_text(
                "❌ Error processing payment. Please contact support.",
                reply_markup=create_main_keyboard(),
                parse_mode='Markdown'
            )
            return MAIN_MENU
        
        # Send VPN accounts to user
        await self._send_vpn_to_user(user_id, vpn_name, vpn_accounts, order_id, context)
        
        # Send confirmation message
        confirmation_text = f"""
✅ *Purchase Successful!*

📦 *Order Details:*
• Order ID: `{order_id}`
• VPN: {vpn_name}
• Quantity: {quantity}
• Total Price: ৳{total_price}
• Status: ✅ Delivered
• Time: {datetime.datetime.now().strftime('%H:%M:%S')}

💰 *Balance Updated:*
• Previous: ৳{user_balance}
• Deducted: ৳{total_price}
• New Balance: ৳{new_balance}

👇 *Your VPN Details Sent Separately* 👇
        """
        
        await query.edit_message_text(
            confirmation_text,
            parse_mode='Markdown'
        )
        
        # Send follow-up message
        followup_text = f"""
🎉 *{quantity} {vpn_name} Account{'s' if quantity > 1 else ''} Delivered!*

*📝 Instructions:*
1. Save all VPN details securely
2. Each account valid for 7 days
3. For setup help, contact {SUPPORT_USERNAME}
4. Order ID: `{order_id}`

*💡 Tips:*
• Use official VPN client
• Contact support for any issues
• Accounts are unique and non-transferable

Want to buy more?
        """
        
        keyboard = [
            [InlineKeyboardButton("🛒 Buy More VPN", callback_data='buy_vpn'),
             InlineKeyboardButton("💰 Check Balance", callback_data='my_balance')],
            [InlineKeyboardButton("📞 Support", url=f'https://t.me/{SUPPORT_USERNAME.replace("@", "")}'),
             InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        
        await context.bot.send_message(
            chat_id=user_id,
            text=followup_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        # Notify admin
        await self._notify_admin(order_id, vpn_name, quantity, total_price, query.from_user)
        
        return MAIN_MENU
    
    async def _send_vpn_to_user(self, user_id: int, vpn_name: str, vpn_accounts: List[str], 
                               order_id: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Send VPN accounts to user with activation codes"""
        try:
            # Create formatted message
            vpn_message = f"""
🔐 *{vpn_name} Accounts*
📦 Order ID: `{order_id}`
📅 Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📞 Support: {SUPPORT_USERNAME}

*📝 FORMAT EXPLANATION:*
• `username:password` → Username and password
• `activation_code` → Just activation code
• `email:password:code` → Email, password and code
• `email:code` → Email and activation code

"""
            
            for i, account in enumerate(vpn_accounts, 1):
                # Parse account data with different formats
                parts = account.split(':')
                
                if len(parts) == 1:
                    # Format 1: Just activation code
                    # Example: ABC123-DEF456-GHI789
                    activation_code = parts[0]
                    
                    vpn_message += f"""
*Account #{i}:*
┌ Type: 📱 Activation Code
├ Code: `{activation_code}`
└ How to use: Enter in VPN app activation section

"""
                
                elif len(parts) == 2:
                    # Format 2: Could be:
                    # 1. username:password
                    # 2. email:password  
                    # 3. email:activation_code
                    # 4. activation_code:server
                    
                    # Check if it looks like an activation code (contains dashes or is alphanumeric)
                    if '-' in parts[0] or (len(parts[0]) >= 12 and parts[0].isalnum()):
                        # Format: activation_code:server
                        activation_code = parts[0]
                        server = parts[1]
                        
                        vpn_message += f"""
*Account #{i}:*
┌ Type: 📱 Activation Code
├ Code: `{activation_code}`
├ Server: `{server}`
└ How to use: Enter code in VPN app

"""
                    
                    elif '@' in parts[0]:
                        # Format: email:activation_code or email:password
                        email = parts[0]
                        if '-' in parts[1] or (len(parts[1]) >= 12 and parts[1].isalnum()):
                            # email:activation_code
                            activation_code = parts[1]
                            vpn_message += f"""
*Account #{i}:*
┌ Type: 📧 Email + Code
├ Email: `{email}`
├ Activation Code: `{activation_code}`
└ How to use: Login with email, then enter code

"""
                        else:
                            # email:password
                            password = parts[1]
                            vpn_message += f"""
*Account #{i}:*
┌ Type: 📧 Email Account
├ Email: `{email}`
├ Password: `{password}`
└ How to use: Login directly with email/password

"""
                    
                    else:
                        # Format: username:password
                        username = parts[0]
                        password = parts[1]
                        vpn_message += f"""
*Account #{i}:*
┌ Type: 👤 Username Account
├ Username: `{username}`
├ Password: `{password}`
└ How to use: Login directly with username/password

"""
                
                elif len(parts) == 3:
                    # Format 3: Could be:
                    # 1. username:password:server
                    # 2. email:password:activation_code
                    # 3. activation_code:server:expiry
                    
                    if '@' in parts[0] and '-' in parts[2]:
                        # Format: email:password:activation_code
                        email = parts[0]
                        password = parts[1]
                        activation_code = parts[2]
                        
                        vpn_message += f"""
*Account #{i}:*
┌ Type: 📧 Full Account
├ Email: `{email}`
├ Password: `{password}`
├ Activation Code: `{activation_code}`
└ How to use: Login with email/password, then activate with code

"""
                    
                    elif '-' in parts[0]:
                        # Format: activation_code:server:expiry
                        activation_code = parts[0]
                        server = parts[1]
                        expiry = parts[2]
                        
                        vpn_message += f"""
*Account #{i}:*
┌ Type: 📱 Activation Code
├ Code: `{activation_code}`
├ Server: `{server}`
├ Expires: `{expiry}`
└ How to use: Enter code in VPN app

"""
                    
                    else:
                        # Format: username:password:server
                        username = parts[0]
                        password = parts[1]
                        server = parts[2]
                        
                        vpn_message += f"""
*Account #{i}:*
┌ Type: 👤 Username Account
├ Username: `{username}`
├ Password: `{password}`
├ Server: `{server}`
└ How to use: Login directly with username/password

"""
                
                elif len(parts) == 4:
                    # Format 4: username:password:server:expiry or email:password:code:expiry
                    username_email = parts[0]
                    password = parts[1]
                    server_code = parts[2]
                    expiry = parts[3]
                    
                    if '@' in username_email and '-' in server_code:
                        # email:password:activation_code:expiry
                        vpn_message += f"""
*Account #{i}:*
┌ Type: 📧 Email Account with Code
├ Email: `{username_email}`
├ Password: `{password}`
├ Activation Code: `{server_code}`
├ Expires: `{expiry}`
└ How to use: Login then activate with code

"""
                    else:
                        # username:password:server:expiry
                        vpn_message += f"""
*Account #{i}:*
┌ Type: 👤 Username Account
├ Username: `{username_email}`
├ Password: `{password}`
├ Server: `{server_code}`
├ Expires: `{expiry}`
└ How to use: Login directly with username/password

"""
            
            vpn_message += f"""
*🔧 Setup Instructions:*

*For Activation Codes:*
1. Download VPN app from official website
2. Open app and find "Activate" or "Redeem Code" option
3. Enter activation code
4. Follow on-screen instructions

*For Username/Password:*
1. Download VPN app
2. Open app and click "Login"
3. Enter username and password
4. Select server and connect

*For Email Accounts:*
1. Download VPN app  
2. Click "Login with Email"
3. Enter email and password
4. If asked for activation code, enter provided code

*⚠️ Important:*
• Keep these credentials secure
• Do not share with others
• Contact {SUPPORT_USERNAME} for help
• Accounts valid for 7 days from activation
            """
            
            # Send to user
            await context.bot.send_message(
                chat_id=user_id,
                text=vpn_message,
                parse_mode='Markdown'
            )
            
            return True
        except Exception as e:
            logger.error(f"Error sending VPN to user {user_id}: {e}")
            return False
    
    async def show_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user balance"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        await query.edit_message_text(
            get_balance_text(user_id, self.balance_manager),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 How to Add Balance", callback_data='payment_info')],
                [InlineKeyboardButton("🛒 Buy VPN", callback_data='buy_vpn'),
                 InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]),
            parse_mode='Markdown'
        )
        return MAIN_MENU
    
    async def show_payment_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show payment information"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        await query.edit_message_text(
            get_payment_info_text(user_id),
            reply_markup=create_payment_info_keyboard(),
            parse_mode='Markdown'
        )
        return PAYMENT_INFO
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            get_help_text(),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📞 Contact Support", url=f'https://t.me/{SUPPORT_USERNAME.replace("@", "")}')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]),
            parse_mode='Markdown'
        )
        return MAIN_MENU
    
    async def show_orders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user orders"""
        query = update.callback_query
        await query.answer()
        
        orders_text = """
📋 *Order History*

*Note:* Detailed order history coming soon!
For now, please save your VPN details when received.

*Current Features:*
• Instant VPN delivery
• Balance tracking
• Multiple VPN options
• Quantity selection (1-10)

*📞 For order inquiries:* Contact support with your Order ID.
        """
        
        await query.edit_message_text(
            orders_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Buy VPN", callback_data='buy_vpn')],
                [InlineKeyboardButton("💰 Check Balance", callback_data='my_balance'),
                 InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]),
            parse_mode='Markdown'
        )
        return MAIN_MENU
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show admin menu"""
        query = update.callback_query
        await query.answer()
        
        user = query.from_user
        
        if user.id != ADMIN_ID:
            await query.edit_message_text(
                "❌ *Access Denied!*\n\nThis menu is for administrators only.",
                reply_markup=create_main_keyboard(),
                parse_mode='Markdown'
            )
            return MAIN_MENU
        
        admin_text = f"""
⚡ *Admin Dashboard*

*Welcome, {user.first_name}!*

*Available Commands:*
• `/addbalance [user_id] [amount]` - Add balance to user
• `/checkbalance [user_id]` - Check user balance
• `/addvpn [type] [accounts]` - Add VPN stock
• `/viewstock` - View VPN stock

*Quick Actions:*
        """
        
        await query.edit_message_text(
            admin_text,
            reply_markup=create_admin_keyboard(),
            parse_mode='Markdown'
        )
        return ADMIN_MENU
    
    async def admin_view_stock(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin: View VPN stock"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            return MAIN_MENU
        
        stock_text = self.vpn_manager.view_all_vpn()
        
        await query.edit_message_text(
            stock_text,
            reply_markup=create_admin_keyboard(),
            parse_mode='Markdown'
        )
        return ADMIN_MENU
    
    async def admin_add_balance_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin: Show add balance instructions"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            return MAIN_MENU
        
        add_balance_text = """
👤 *Add User Balance*

*Usage:* `/addbalance [user_id] [amount]`

*Example:* 
`/addbalance 123456789 500`
(This adds ৳500 to user's account)

*User will receive notification when balance is added.*
        """
        
        await query.edit_message_text(
            add_balance_text,
            reply_markup=create_admin_keyboard(),
            parse_mode='Markdown'
        )
        return ADMIN_MENU
    
    async def admin_add_vpn_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin: Show add VPN instructions"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            return MAIN_MENU
        
        add_vpn_text = """
➕ *Add VPN Stock*

*Usage:* `/addvpn [type] [accounts]`

*Example:* 
`/addvpn nord user1:pass123:server1 user2:pass456:server2`

*Available Types:* nord, surfshark, cyberghost, expressvpn, hma, proton, ipvanish, vyper, panda, hotspot, norton

*📝 FORMATS SUPPORTED:*
1. *Activation Code Only:* `ABC123-DEF456-GHI789`
2. *Username/Password:* `username:password`
3. *Email/Password:* `email@gmail.com:password123`
4. *Email/Code:* `email@gmail.com:ABC123-DEF456`
5. *Full Account:* `email:password:activation_code`
6. *With Server:* `activation_code:server_name`
7. *With Expiry:* `username:password:server:2024-12-31`

*💡 For activation codes, just add the code alone.*
        """
        
        await query.edit_message_text(
            add_vpn_text,
            reply_markup=create_admin_keyboard(),
            parse_mode='Markdown'
        )
        return ADMIN_MENU
    
    async def admin_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin: Show statistics"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            return MAIN_MENU
        
        # Get user count from balance file
        user_count = 0
        try:
            if os.path.exists("user_balance.json"):
                with open("user_balance.json", 'r') as f:
                    balances = json.load(f)
                    user_count = len(balances)
        except:
            pass
        
        stats_text = f"""
📈 *Statistics Dashboard*

*🤖 Bot Information:*
• Active: ✅ Running
• VPN Types: 11  # UPDATED
• Price: ৳{VPN_PRICE_TAKA} per VPN

*📊 VPN Stock:* {self.vpn_manager.view_all_vpn()}

*👥 User Statistics:*
• Total Users: {user_count}
• Admin: {SUPPORT_USERNAME}

*💡 Note:* Detailed analytics coming soon!
        """
        
        await query.edit_message_text(
            stats_text,
            reply_markup=create_admin_keyboard(),
            parse_mode='Markdown'
        )
        return ADMIN_MENU
    
    # ==================== COMMAND HANDLERS ====================
    
    async def addbalance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /addbalance command"""
        user = update.effective_user
        
        if user.id != ADMIN_ID:
            await update.message.reply_text(
                "❌ This command is for administrators only.",
                parse_mode='Markdown'
            )
            return
        
        if len(context.args) != 2:
            await update.message.reply_text(
                "❌ *Usage:* `/addbalance [user_id] [amount]`\n"
                "*Example:* `/addbalance 123456789 500`",
                parse_mode='Markdown'
            )
            return
        
        try:
            user_id = int(context.args[0])
            amount = int(context.args[1])
            
            if amount <= 0:
                await update.message.reply_text(
                    "❌ Amount must be greater than 0.",
                    parse_mode='Markdown'
                )
                return
            
            success, new_balance = self.balance_manager.add_balance(user_id, amount)
            
            if success:
                await update.message.reply_text(
                    f"✅ *Balance Added Successfully!*\n\n"
                    f"• User ID: `{user_id}`\n"
                    f"• Amount Added: ৳{amount}\n"
                    f"• New Balance: ৳{new_balance}\n\n"
                    f"User can now buy {new_balance // VPN_PRICE_TAKA} VPN(s)",
                    parse_mode='Markdown'
                )
                
                # Notify user
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"🎉 *Balance Added!*\n\n"
                             f"৳{amount} has been added to your account.\n"
                             f"*New Balance:* ৳{new_balance}\n\n"
                             f"You can now buy {new_balance // VPN_PRICE_TAKA} VPN(s)\n\n"
                             f"Thank you for your payment!\n"
                             f"📞 Support: {SUPPORT_USERNAME}",
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    logger.error(f"Could not notify user {user_id}: {e}")
                    await update.message.reply_text(
                        f"⚠️ *User Notification Failed*\n"
                        f"User might have blocked the bot or ID is incorrect.",
                        parse_mode='Markdown'
                    )
            else:
                await update.message.reply_text(
                    "❌ Error adding balance. Please try again.",
                    parse_mode='Markdown'
                )
                
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid user ID or amount. Please check and try again.",
                parse_mode='Markdown'
            )
    
    async def checkbalance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /checkbalance command"""
        user = update.effective_user
        
        if user.id != ADMIN_ID:
            await update.message.reply_text(
                "❌ This command is for administrators only.",
                parse_mode='Markdown'
            )
            return
        
        if len(context.args) != 1:
            await update.message.reply_text(
                "❌ *Usage:* `/checkbalance [user_id]`\n"
                "*Example:* `/checkbalance 123456789`",
                parse_mode='Markdown'
            )
            return
        
        try:
            user_id = int(context.args[0])
            balance = self.balance_manager.get_balance(user_id)
            
            await update.message.reply_text(
                f"💰 *User Balance*\n\n"
                f"• User ID: `{user_id}`\n"
                f"• Current Balance: ৳{balance}\n"
                f"• Can buy: {balance // VPN_PRICE_TAKA} VPN(s)\n"
                f"• In USD: ${round(balance * 0.008, 2)}",
                parse_mode='Markdown'
            )
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid user ID.",
                parse_mode='Markdown'
            )
    
    async def addvpn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /addvpn command"""
        user = update.effective_user
        
        if user.id != ADMIN_ID:
            await update.message.reply_text(
                "❌ This command is for administrators only.",
                parse_mode='Markdown'
            )
            return
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ *Usage:* `/addvpn [type] [account1] [account2] ...`\n\n"
                "*Example:* \n"
                "• For activation codes: `/addvpn nord ABC123-DEF456-GHI789 JKL012-MNO345-PQR678`\n"
                "• For accounts: `/addvpn nord user1:pass1:server1 user2:pass2:server2`\n\n"
                "*Available Types:* nord, surfshark, cyberghost, expressvpn, hma, proton, ipvanish, vyper, panda, hotspot, norton\n"
                "*Format:* Supports activation codes, username/password, email/password, etc.",
                parse_mode='Markdown'
            )
            return
        
        vpn_type = context.args[0].lower()
        accounts = context.args[1:]
        
        valid_types = ['nord', 'surfshark', 'cyberghost', 'expressvpn', 'hma', 'proton', 'ipvanish', 'vyper', 'panda', 'hotspot', 'norton']  # UPDATED
        
        if vpn_type not in valid_types:
            await update.message.reply_text(
                f"❌ Invalid VPN type. Available types: {', '.join(valid_types)}",
                parse_mode='Markdown'
            )
            return
        
        success = self.vpn_manager.add_vpn_account(vpn_type, accounts)
        
        if success:
            new_count = self.vpn_manager.get_vpn_count(vpn_type)
            await update.message.reply_text(
                f"✅ *VPN Accounts Added!*\n\n"
                f"• Type: {vpn_type.capitalize()}\n"
                f"• Added: {len(accounts)} accounts\n"
                f"• Total Stock: {new_count} accounts\n\n"
                f"*Format Detected:*\n"
                f"First account: `{accounts[0]}`",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ Error adding VPN accounts. Please check the format and try again.",
                parse_mode='Markdown'
            )
    
    async def viewstock_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /viewstock command"""
        user = update.effective_user
        
        if user.id != ADMIN_ID:
            await update.message.reply_text(
                "❌ This command is for administrators only.",
                parse_mode='Markdown'
            )
            return
        
        stock_text = self.vpn_manager.view_all_vpn()
        
        await update.message.reply_text(
            stock_text,
            parse_mode='Markdown'
        )
    
    async def _notify_admin(self, order_id: str, vpn_name: str, quantity: int, 
                           total_price: int, user):
        """Notify admin about new order"""
        try:
            admin_text = f"""
🛒 *New VPN Order!*

📦 *Order Details:*
• Order ID: `{order_id}`
• VPN: {vpn_name}
• Quantity: {quantity}
• Total: ৳{total_price}
• User: {user.first_name} (@{user.username})
• User ID: `{user.id}`
• Time: {datetime.datetime.now().strftime('%H:%M:%S')}

✅ *Status:* Auto-Delivered
            """
            
            await self.application.bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Admin notification error: {e}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        try:
            if update.callback_query:
                await update.callback_query.message.reply_text(
                    "❌ An error occurred. Please try again or contact support.",
                    reply_markup=create_main_keyboard()
                )
        except:
            pass
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("addbalance", self.addbalance_command))
        self.application.add_handler(CommandHandler("checkbalance", self.checkbalance_command))
        self.application.add_handler(CommandHandler("addvpn", self.addvpn_command))
        self.application.add_handler(CommandHandler("viewstock", self.viewstock_command))
        
        # Callback query handlers with proper state management
        self.application.add_handler(CallbackQueryHandler(self.main_menu, pattern='^main_menu$'))
        self.application.add_handler(CallbackQueryHandler(self.buy_vpn, pattern='^buy_vpn$'))
        self.application.add_handler(CallbackQueryHandler(self.select_vpn_type, pattern='^select_'))
        self.application.add_handler(CallbackQueryHandler(self.select_quantity, pattern='^qty_'))
        self.application.add_handler(CallbackQueryHandler(self.show_balance, pattern='^my_balance$'))
        self.application.add_handler(CallbackQueryHandler(self.show_payment_info, pattern='^payment_info$'))
        self.application.add_handler(CallbackQueryHandler(self.show_help, pattern='^help$'))
        self.application.add_handler(CallbackQueryHandler(self.show_orders, pattern='^my_orders$'))
        self.application.add_handler(CallbackQueryHandler(self.admin_menu, pattern='^admin_menu$'))
        self.application.add_handler(CallbackQueryHandler(self.admin_view_stock, pattern='^admin_view_stock$'))
        self.application.add_handler(CallbackQueryHandler(self.admin_add_balance_menu, pattern='^admin_add_balance$'))
        self.application.add_handler(CallbackQueryHandler(self.admin_add_vpn_menu, pattern='^admin_add_vpn$'))
        self.application.add_handler(CallbackQueryHandler(self.admin_stats, pattern='^admin_stats$'))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    def run(self):
        """Run the bot"""
        print("🤖 Starting VPN Selling Bot...")
        print("=" * 50)
        print(f"🔑 Token: {BOT_TOKEN[:15]}...")
        print(f"👑 Admin ID: {ADMIN_ID}")
        print(f"📞 Support: {SUPPORT_USERNAME}")
        print(f"💰 VPN Price: ৳{VPN_PRICE_TAKA} each")
        print(f"🌐 VPN Types: 11 different services")  # UPDATED
        print("=" * 50)
        
        # Create VPN folder and files if not exist
        os.makedirs(VPN_FOLDER, exist_ok=True)
        for file_path in [NORD_FILE, SURFSHARK_FILE, CYBERGHOST_FILE, EXPRESSVPN_FILE,
                         HMA_FILE, PROTON_FILE, IPVANISH_FILE, VYPER_FILE, PANDA_FILE, 
                         HOTSPOT_FILE, NORTON_FILE]:  # UPDATED
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    pass
                print(f"✅ Created {file_path}")
        
        # Create balance file if not exist
        if not os.path.exists("user_balance.json"):
            with open("user_balance.json", 'w') as f:
                json.dump({}, f)
            print("✅ Created user_balance.json")
        
        # Create application
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Setup handlers
        self.setup_handlers()
        
        print("\n✅ Bot started successfully!")
        print("⏳ Listening for commands...")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)
        
        # Run the bot
        self.application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )

# ==================== MAIN ====================
if __name__ == "__main__":
    bot = VPNBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")