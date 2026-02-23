// Assigned to: Mai Komar
// Phase: 3 (F3.2)
//
// TODO: Message thread component for listing detail page.
//
// Props:
//   - listingId: number
//   - sellerId: number (to determine if current user is seller or buyer)
//
// Structure:
//   <div className="message-thread">
//     <h3>Messages</h3>
//     <div className="messages-list">
//       {messages.map(msg => (
//         <div className={`message ${msg.sender_id === currentUser.id ? 'sent' : 'received'}`}>
//           <span className="message-sender">{msg.sender.name}</span>
//           <p className="message-content">{msg.content}</p>
//           <span className="message-time">{formatted timestamp}</span>
//         </div>
//       ))}
//       {messages.length === 0 && <p>No messages yet. Start the conversation!</p>}
//     </div>
//     <form className="message-form" onSubmit={handleSend}>
//       <input type="text" value={newMessage} onChange={...} placeholder="Type a message..." />
//       <button type="submit">Send</button>
//     </form>
//   </div>
//
// Behavior:
//   1. On mount, call api/messages.ts getMessages(listingId)
//   2. Display messages in chronological order
//   3. Style sent messages (right-aligned) vs received (left-aligned)
//   4. On form submit, call api/messages.ts sendMessage(listingId, { content })
//   5. After sending, append new message to list (or re-fetch)
//   6. Auto-scroll to bottom on new messages
//   7. Don't show message form if user is the seller and no one has messaged yet
