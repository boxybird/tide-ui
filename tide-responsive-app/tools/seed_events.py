"""Author the fixed long-feed fixture. IANA timezone data is needed only to reseed.
Normal HTML builds consume the committed JSON, including its UTC offsets.
"""
from pathlib import Path
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
import json
import re

ROOT=Path(__file__).resolve().parents[1]
# date, category, title, venue, start, admission, age, subtitle, description
ROWS=[
 ('10-24','Workshop','Tiny Prints, Big Ideas','The Paper Table','14:00','$20','All ages','Small blocks. Plenty of possibility.','Make a miniature print from one small carving block. Experiment with simple shapes, then trade a print with someone at the table.'),
 ('10-24','Music','Saturday on the Small Stage','Sister','20:00','$18','21+','Close enough to hear the strings.','Three local acts share a small stage and a generous evening. Expect guitar-led sets, a little improvisation and room to find your favorite corner.'),
 ('10-25','Workshop','Sunday Paper Club','Barelas Print Studio','11:00','Free','All ages','Bring an idea. Borrow some paper.','Drop in with scraps, sketches or nothing at all. The shared table is open for collage, simple stamps and a few hours of making things together.'),
 ('10-25','Music','Low Volume Sunday','Warehouse Room','18:00','$10','All ages','A softer landing for the weekend.','An early evening of acoustic sets with space between the songs. Come for one set or settle in for the whole session.'),
 ('10-26','Comedy','First Drafts & False Starts','Dry Heat','19:00','Free','21+','New material, still finding its feet.','Local comics try out fresh stories in a forgiving room. Some jokes will land, some will become better stories next week.'),
 ('10-27','Workshop','Postcards from the Neighborhood','The Paper Table','18:00','$18','16+','Make something worth sending.','Turn familiar streets, buildings and small observations into a set of hand-printed postcards. Simple designs are very welcome.'),
 ('10-27','Music','Two Guitars, One Room','Warehouse Room','20:00','$12','All ages','An evening without much distance.','Two songwriters trade short sets, favorite songs and the stories behind them. The room is small and the arrangements stay simple.'),
 ('10-28','Comedy','Midweek Mic','Dry Heat','19:00','$8','21+','A good reason to go out on Wednesday.','A rotating host introduces a mix of familiar local voices and first-time performers. Expect short sets and a relaxed pace.'),
 ('10-29','Workshop','Black Ink, Bright Paper','Barelas Print Studio','18:00','$24','18+','One color can do a lot.','Explore contrast with dark ink and a stack of colorful paper. Cut a bold shape, adjust the pressure and see what changes from print to print.'),
 ('10-29','Music','Songs for the Last Light','Warehouse Room','20:00','$15','All ages','For the end of a long day.','An intimate lineup of songs about home, leaving and getting there eventually. Local musicians perform stripped-back sets.'),
 ('10-30','Comedy','The Friday Reset','Dry Heat','19:00','$12','21+','Leave the week at the door.','A hosted evening of local stand-up, everyday frustrations and useful perspective. Arrive early if you want to sit with friends.'),
 ('10-31','Workshop','Carve a Creature','The Paper Table','13:00','$16','All ages','Friendly monsters encouraged.','Design a small creature and turn it into a repeatable paper print. There will be simple stamping options for younger makers.'),
 ('10-31','Music','Costumes & Feedback','Sister','21:00','$20','21+','A little strange. A little loud.','Close October with a roomful of noisy local bands and homemade costumes. Dressing up is welcome, and entirely optional.'),
 ('11-01','Workshop','First Sunday Print Exchange','Barelas Print Studio','11:00','Free','All ages','A fresh month at the shared table.','Bring a few prints to exchange, or stop by to see what people are making. A small demonstration table is open to beginners.'),
 ('11-01','Music','November, Quietly','Warehouse Room','19:00','$10','All ages','An early start to a new month.','A low-key evening of local acoustic music. Short sets leave time to talk, listen and make plans for the weeks ahead.'),
 ('11-02','Comedy','Nothing Personal','Dry Heat','19:00','$10','21+','Stories that got a little out of hand.','Local comics share opinions they probably should have kept to themselves. An easygoing Monday lineup with a host to keep things moving.'),
 ('11-03','Workshop','A Table Full of Zines','The Paper Table','18:00','$12','16+','Fold, print, share, repeat.','Make a tiny folded publication using stamps, collage and a few handwritten lines. Leave with a finished zine and a few copies to trade.'),
 ('11-04','Music','After the Record Store Closes','Sister','20:00','$14','21+','The listening continues.','A pair of local bands bring their favorite influences into a live set. Expect familiar textures and a few things you have not heard before.'),
 ('11-05','Comedy','Setups & Second Chances','Dry Heat','19:00','$8','21+','The first version is never the last.','A workshop-style comedy night where short sets get a second pass. Come for the stories, stay for the changes.'),
 ('11-06','Workshop','Friday Night Ink Club','Barelas Print Studio','18:00','$28','21+','Clock out. Roll some ink.','Spend a Friday evening making a small block print around the shared studio table. Bring a sketch if you have one; there are prompts if you do not.'),
 ('11-06','Music','Analog Hours','Sister','21:00','$20','21+','Warm amps and a late finish.','A night of guitar-driven local music, a few extended instrumentals and plenty of texture. The first set starts soon after doors.'),
 ('11-07','Workshop','Print Something for Someone','The Paper Table','13:00','$22','All ages','A small handmade gesture.','Make a short run of simple prints to give away. Work from a personal symbol, a shared joke or a pattern that feels like someone you know.'),
 ('11-07','Comedy','Small Room, Big Opinions','Dry Heat','21:00','$15','21+','Everyone has a theory.','A Saturday lineup of local comics with strong views about very ordinary things. General admission seating keeps the room relaxed.'),
 ('11-08','Music','Sunday in Slow Motion','Warehouse Room','17:00','$12','All ages','One more song before Monday.','An early show of unhurried local sets. Bring someone who likes to listen, and leave with a little evening still ahead of you.'),
 ('11-09','Workshop','Beginner’s Block','Barelas Print Studio','18:00','$20','16+','Your first print starts here.','Start with the basics of carving, inking and pulling a print. The session moves slowly, with time to practice each step.'),
 ('11-10','Comedy','Ten Minutes Each','Dry Heat','19:00','Free','21+','A few stories. A clear time limit.','A quick-moving lineup gives each comic ten minutes and a chance to try something new. Drop in for an informal weekday show.'),
 ('11-11','Music','Desert Radio Live','Sister','20:00','$18','21+','Local sounds, in the same room.','A varied lineup moves from quiet guitar parts to a fuller late set. Come early to hear the whole progression.'),
 ('11-12','Workshop','The Art of the Imperfect Print: An Evening of Layers, Texture & Happy Accidents','Barelas Print Studio','18:00','$30','18+','Make room for the unexpected.','Explore layered prints, uneven textures and the useful surprises that happen when ink meets paper. Bring curiosity rather than a polished plan.'),
 ('11-13','Comedy','The Very Late Set','Dry Heat','21:30','$15','21+','For people who are not done with Friday.','A late lineup of local stand-up and a relaxed host. Expect adult themes, short sets and a room ready for one more story.'),
 ('11-14','Music','Three Bands & a Borrowed Amp','Sister','20:00','$18','All ages','A shared stage and a few new favorites.','Three local bands split the evening with fast changeovers and distinctly different sounds. One admission covers the full lineup.'),
 ('11-15','Workshop','Paper, Coffee & Company','The Paper Table','11:00','$16','All ages','An unhurried morning of making.','A gentle introduction to printing simple patterns on paper. Work at your own pace and enjoy the company around the table.'),
 ('11-16','Comedy','Notes from the Group Chat','Dry Heat','19:00','$12','21+','Some things sound better out loud.','Local comics turn everyday messages, misunderstandings and family updates into an evening of stand-up.'),
 ('11-17','Workshop','Two Colors, One Block','Barelas Print Studio','18:00','$26','16+','A little planning. A little overlap.','Try a two-color print with one simple block. Explore how small shifts in alignment and color change the finished image.'),
 ('11-18','Music','Near the Speakers','Sister','20:00','$16','21+','For the songs that sound better live.','An evening of local bands built around a small room and a close audience. Find a spot where the mix feels right to you.'),
 ('11-19','Comedy','Warm-Up Night','Dry Heat','19:00','$8','21+','Fresh material before the weekend.','A Thursday room for comics to test new ideas and audiences to discover a few new voices. The host keeps the sets short.'),
 ('11-20','Workshop','After Work, Make Something','Barelas Print Studio','18:00','$24','21+','A different use for your hands.','Put the workday aside and make a small set of printed cards. All the basic tools are ready at the table.'),
 ('11-21','Music','The Neighborhood Listening Room','Warehouse Room','20:00','$12','All ages','A seat near a good song.','An intimate evening of local songwriters and small arrangements. Between songs there is room for a story or two.'),
 ('11-22','Workshop','Handmade Holiday Cards','The Paper Table','14:00','$22','All ages','Start with paper. End with a small stack.','Print a personal pattern or a simple message onto a set of blank cards. There are plenty of non-seasonal prompts too.'),
 ('11-23','Comedy','A Few Good Stories','Dry Heat','19:00','$10','21+','The ones worth telling again.','Local comics bring longer stories to a relaxed Monday room. Expect a little more detail and a few unexpected endings.'),
 ('11-24','Workshop','Print Swap & Studio Social','Barelas Print Studio','18:00','Free','All ages','See what everyone has been making.','An open studio evening for showing work, trading a print and asking questions. Come to browse even if you have nothing to exchange.'),
 ('11-25','Music','Home for the Long Weekend','Sister','20:00','$18','21+','Familiar faces, a shared evening.','Local musicians and returning friends share short sets before the long weekend. One ticket covers the full evening.'),
 ('11-26','Music','An Open Door Session','Warehouse Room','16:00','Free','All ages','Come in for a song or two.','An informal afternoon of acoustic music. Stay for a short set or settle into a quiet corner for the whole session.'),
 ('11-27','Comedy','Leftovers & One-Liners','Dry Heat','21:30','$12','21+','A late show after a long week.','A relaxed Friday lineup finds the funny side of family gatherings, too much food and unusual holiday plans.'),
 ('11-28','Workshop','Make Your Own Gift Wrap','The Paper Table','13:00','$18','All ages','Good paper deserves a second life.','Use simple stamps to turn plain paper into reusable wrapping sheets. Try a repeating pattern or make every sheet different.'),
 ('11-29','Music','One More Sunday','Warehouse Room','18:00','$12','All ages','A soft close to the month.','Finish November with a small lineup of local acoustic sets. An early start leaves time to get home without rushing.')
]


def clock(value):return f'{(value.hour-1)%12+1}:{value.minute:02d} '+('AM' if value.hour<12 else 'PM')


def main():
    zone=ZoneInfo('America/Denver')
    events=json.loads((ROOT/'data/events-core.json').read_text(encoding='utf-8'))
    for date,category,title,venue,start,price,age,subtitle,lead in ROWS:
        begin=datetime.fromisoformat('2026-'+date+'T'+start).replace(tzinfo=zone)
        minutes=90 if category=='Comedy' else 120
        end=begin+timedelta(minutes=minutes)
        slug=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')
        if len(slug)>62:slug='the-imperfect-print'
        image={'Music':'concert.png','Comedy':'comedy.png','Workshop':'ink-after-dark.png'}[category]
        alt={'Music':events[0]['alt'],'Comedy':events[1]['alt'],'Workshop':events[2]['alt']}[category]
        if category=='Workshop':
            inclusions=['Shared tools, ink and paper','Guidance from a local printmaker','Your finished work to take home']
            schedule=[(0,'Meet the table and choose a direction'),(20,'Work on your design'),(60,'Print, compare and try another version'),(minutes,'Pack up and share what you made')]
            know=['No previous printmaking experience is needed. Wear something you would be happy to get ink on.','All ages are welcome; younger makers should come with an adult.' if age=='All ages' else f'This session is {age}. Arrive about ten minutes early to get settled.']
            heading='An idea, a table and a little ink.';eyebrow='At the worktable'
        elif category=='Comedy':
            inclusions=['A hosted lineup of local comedians','General admission seating','A 90-minute evening of stand-up']
            schedule=[(-20,'Doors and seating'),(0,'Your host opens the show'),(15,'The lineup takes the mic'),(minutes,'Good nights and last laughs')]
            know=['Seats are first come, first served. Arrive before the show to sit together.','Expect adult language and themes. This is a 21+ show; please keep phones silent during sets.']
            heading='Make a little room for a good laugh.';eyebrow='In good company'
        else:
            inclusions=['Two hours of local live music','One admission for the full lineup','Time between sets to find your favorite spot']
            schedule=[(-30,'Doors open'),(0,'The first set'),(60,'A short break and the next act'),(minutes,'Last songs and good nights')]
            know=['Set times are approximate. Bring hearing protection if you prefer a quieter listening experience.','All ages are welcome in this sample listing. Check seating and venue arrangements before making plans.' if age=='All ages' else 'This is a 21+ evening. Bring photo identification and check the venue’s admission details before heading out.']
            heading='Local sounds. A room worth finding.';eyebrow='In the room'
        # Long and short detail examples without changing the component template.
        if title.startswith('The Art of the Imperfect'):
            know.extend(['You can start from a supplied shape or bring a small sketch. Keep designs simple enough to finish in one session.','Work dries on a shared rack while you explore another variation. Bring a flat folder if you would like to carry your prints home without folding them.'])
        events.append(dict(slug=slug,title=title,category=category,venue=venue,date=begin.date().isoformat(),start=start,time=clock(begin),range=clock(begin)+'–'+clock(end),duration='90 minutes' if minutes==90 else '2 hours',price=price,included='Free entry' if price=='Free' else 'Materials included' if category=='Workshop' else 'Seated show' if category=='Comedy' else 'General admission',age=age,subtitle=subtitle,image=image,alt=alt,eyebrow=eyebrow,heading=heading,lead=lead,inclusions=inclusions,schedule=[(clock(begin+timedelta(minutes=offset)),text) for offset,text in schedule],know=know,attendance=('Entry is free. ' if price=='Free' else f'Admission is {price}. ')+('Materials and tools are included. ' if category=='Workshop' and price!='Free' else '')+'This is an illustrative event. A real listing would link to the organizer for availability, fees and cancellation terms.'))
    for event in events:
        begin=datetime.fromisoformat(event['date']+'T'+event['start']).replace(tzinfo=zone)
        event.update(day=str(begin.day),weekday=begin.strftime('%a'),longDate=f'{begin:%A}, {begin:%B} {begin.day}',datetime=begin.isoformat(),month=begin.strftime('%b'))
    events.sort(key=lambda x:(x['date'],x['start'],x['slug']))
    assert len(events)==48 and len({x['slug'] for x in events})==48
    (ROOT/'data/events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('48 authored sample events: 16 in October, 32 in November.')


if __name__=='__main__':main()
