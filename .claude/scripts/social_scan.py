#!/usr/bin/env python3
"""Social Scan — AIパク宛メッセージの検出"""
import json
import subprocess
import os

ROOMS = {
    "407274282": "ぎいちゃん編集部屋",
    "369212015": "なるみさん編集部屋",
    "412287082": "1st BLN",
    "423036437": "Claude Code DIVE",
    "382622982": "DIVE SYNC",
}

AIPARK_ACCOUNT_ID = 7115249

def get_token():
    result = subprocess.run(
        ["zsh", "-i", "-c", "echo $CHATWORK_API_TOKEN"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def get_messages(room_id, token):
    result = subprocess.run(
        ["curl", "-s", f"https://api.chatwork.com/v2/rooms/{room_id}/messages?force=1",
         "-H", f"X-ChatWorkToken: {token}"],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout)
    except:
        return []

def scan():
    token = get_token()
    if not token:
        print("ERROR: CHATWORK_API_TOKEN not found")
        return

    all_findings = []

    for room_id, room_name in ROOMS.items():
        msgs = get_messages(room_id, token)
        if not isinstance(msgs, list):
            continue

        # Find AIパク messages and responses after them
        aipark_indices = []
        for i, m in enumerate(msgs):
            aid = m.get("account", {}).get("account_id", 0)
            body = m.get("body", "")
            if aid == AIPARK_ACCOUNT_ID and "[info]" in body:
                aipark_indices.append(i)

        # Check for replies after AIパク messages
        for idx in aipark_indices:
            for j in range(idx + 1, len(msgs)):
                reply_msg = msgs[j]
                reply_aid = reply_msg.get("account", {}).get("account_id", 0)
                reply_body = reply_msg.get("body", "")
                reply_name = reply_msg.get("account", {}).get("name", "unknown")

                if reply_aid == AIPARK_ACCOUNT_ID:
                    # AIパク's own follow-up, skip but also means subsequent are not "unreplied"
                    break

                # Check if this is a reply to AIパク
                is_reply_to_aipark = f"[rp aid={AIPARK_ACCOUNT_ID}" in reply_body
                is_mention = any(kw in reply_body for kw in ["AIパク", "aiパク", "AI パク", "AIぱく", "Aiパク"])
                is_after_aipark = True  # It's after an AIパク message

                if is_reply_to_aipark or is_mention or is_after_aipark:
                    # Check if AIパク already replied after this
                    already_replied = False
                    for k in range(j + 1, len(msgs)):
                        if msgs[k].get("account", {}).get("account_id", 0) == AIPARK_ACCOUNT_ID:
                            already_replied = True
                            break

                    if not already_replied:
                        body_preview = reply_body[:200].replace("\n", " ")
                        all_findings.append({
                            "room_id": room_id,
                            "room_name": room_name,
                            "sender_name": reply_name,
                            "sender_id": reply_aid,
                            "body_preview": body_preview,
                            "send_time": reply_msg.get("send_time", 0),
                            "message_id": reply_msg.get("message_id", ""),
                        })

        # Also check for direct AIパク mentions not tied to a reply
        for m in msgs[-10:]:
            aid = m.get("account", {}).get("account_id", 0)
            body = m.get("body", "")
            name = m.get("account", {}).get("name", "unknown")

            if aid != AIPARK_ACCOUNT_ID:
                is_mention = any(kw in body for kw in ["AIパク", "aiパク", "AI パク", "AIぱく", "Aiパク"])
                if is_mention:
                    # Check not already in findings
                    mid = m.get("message_id", "")
                    if not any(f["message_id"] == mid for f in all_findings):
                        # Check if AIパク replied after
                        msg_time = m.get("send_time", 0)
                        already_replied = False
                        for later in msgs:
                            if (later.get("account", {}).get("account_id", 0) == AIPARK_ACCOUNT_ID
                                and later.get("send_time", 0) > msg_time):
                                already_replied = True
                                break
                        if not already_replied:
                            body_preview = body[:200].replace("\n", " ")
                            all_findings.append({
                                "room_id": room_id,
                                "room_name": room_name,
                                "sender_name": name,
                                "sender_id": aid,
                                "body_preview": body_preview,
                                "send_time": msg_time,
                                "message_id": mid,
                            })

    # Output results as JSON
    print(json.dumps(all_findings, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    scan()
