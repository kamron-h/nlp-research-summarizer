css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.wikia.nocookie.net%2Favp%2Fimages%2Fa%2Fa8%2FDavidcovenant.jpg%2Frevision%2Flatest%3Fcb%3D20170527212857&f=1&nofb=1&ipt=04f4281e03062cd3865963145833e3ec1bd1f961404edf62a0dae8df52631a1a&ipo=images" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        <div style="margin-left:1.3em"><p>David</p></div>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdenovosoftware.com%2Fwp-content%2Fuploads%2Fface-placeholder.png&f=1&nofb=1&ipt=19dc5fbaafb063c8f717bbd29c89904adf8f3ce5a2cd74fa4971c860cc737628&ipo=images">
        <div style="margin-left:1.5em"><p>User</p></div>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
