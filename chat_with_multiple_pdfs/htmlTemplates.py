css = '''
<style>
.chat-message {
    padding: 1.2rem; /* Increased padding for more emphasis */
    border-radius: 1.2rem; /* Rounded border for a softer look */
    margin-bottom: 2rem; /* Increased margin for better separation */
    display: flex;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Added box shadow for depth */
}
.chat-message.user {
    background-color: #ff6f61; /* Vibrant coral background for user messages */
}
.chat-message.bot {
    background-color: #74b3ce; /* Calming blue background for bot messages */
}
.chat-message .avatar {
    width: 20%; /* Maintained avatar size */
}
.chat-message .avatar img {
    max-width: 60px; /* Adjusted avatar image max-width */
    max-height: 60px; /* Adjusted avatar image max-height */
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 80%; /* Adjusted message width */
    padding: 1rem; /* Balanced padding for better readability */
    color: #333; /* Changed text color for better contrast */
    font-weight: bold; /* Added bold font for emphasis */
    font-family: 'Arial', sans-serif; /* Changed font family for clarity */
    text-transform: uppercase; /* Uppercase text for a stylish look */
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://th.bing.com/th/id/OIP.pC__yzOdh1hAPl44jxhSQQHaE8?rs=1&pid=ImgDetMain" width="120" height="120" style="border-radius: 50%;"> <!-- Rounded image -->
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://th.bing.com/th/id/OIP.XQRkIBC22dONu12hlg7v2gHaHd?rs=1&pid=ImgDetMain" width="120" height="120" style="border-radius: 50%;"> <!-- Rounded image -->
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''