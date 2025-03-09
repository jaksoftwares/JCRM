from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ministry, MinistryMembership
from events.models import Event  # Importing events from the Events app
from .forms import MinistryMembershipForm


def index(request):
    ministries_image_base_url = "images/ministries"
    def buildImagePath(path:str) -> str:
        return "{baseUrl}/{path}".format(baseUrl=ministries_image_base_url,path=path)
    ministries = [
        {
            "title": "Worship & Creative Arts Ministries",
            "description": "The Worship Team leads the congregation in heartfelt praise and worship during services. The Media & Production Team supports our services through live streams, photography, and video production, and the Drama & Creative Arts Ministry allows members to express their faith through artistic performances.",
            "image_url": buildImagePath("praiseImg1.jpeg")
        },
        {
            "title": "Discipleship & Christian Growth Ministries",
            "description": "Bible Study Groups offer small group fellowships for in-depth Bible study and prayer, while the Prayer Ministry brings together intercessors to pray for the needs of the church and community. The New Believers’ Class is designed to guide those new to the faith in their spiritual journey.",
            "image_url": buildImagePath("bibleStudyImg.png")
        },
        {
            "title": "Outreach & Evangelism Ministries",
            "description": "The Evangelism & Missions team spreads the Gospel locally and globally, while the Community Outreach ministry serves the needy through food drives, clothing donations, and other initiatives.",
            "image_url": buildImagePath("evangelismImg.png")
        },
        {
            "title": "Life & Family Groups",
            "description": "The Men’s Ministry empowers men to grow in their faith and build strong relationships, while the Women’s Ministry offers fellowship, mentorship, and empowerment for women. The Youth Ministry guides teenagers and young adults in their spiritual walk, and the Children’s Ministry teaches kids biblical truths in fun and engaging ways",
            "image_url": buildImagePath("familyGroupsImg.jpeg")
        },
        {
            "title": "Service & Support Ministries",
            "description": "Our Service & Support Ministries play a vital role in creating a seamless and welcoming environment for everyone who walks through our doors. These ministries work behind the scenes to ensure that every service, event, and activity runs smoothly, allowing the church to function effectively and remain a safe, inviting space for all.",
            "image_url": buildImagePath("supportImg.jpeg")
        }
    ]

    get_involved_actions = [
        {
            "title":"Visit us this sunday",
            "description":"Come and worship with us",
            "icon_path":buildImagePath("vectors/rocket.svg")
        },
        {
            "title":"Become a member",
            "description":"Grow in faith and community",
            "icon_path":buildImagePath("vectors/support.svg")
        },
        {
            "title":"Join a ministry",
            "description":"Use your gifts for God's glory!",
            "icon_path":buildImagePath("vectors/app.svg")
        },
        {
            "title":"Give & support",
            "description":"Partner with us in advancing God's kingdom.",
            "icon_path":buildImagePath("vectors/credit-card.svg")
        }
    ]
    return render(request, 'ministries/index.html',{'ministries': ministries,'get_involved_actions':get_involved_actions})


def ministry_list(request):
    ministries = []
    
    return render(request, 'ministries/ministry_list.html', {'ministries': ministries})

def ministry_detail(request, slug):
    ministry = get_object_or_404(Ministry, slug=slug)
    ministry_events = Event.objects.filter(category__name__icontains=ministry.name)
    return render(request, 'ministries/ministry_detail.html', {'ministry': ministry, 'events': ministry_events})

def join_ministry(request, slug):
    ministry = get_object_or_404(Ministry, slug=slug)
    
    if request.method == 'POST':
        form = MinistryMembershipForm(request.POST)
        if form.is_valid():
            membership = form.save(commit=False)
            membership.ministry = ministry
            membership.save()
            return redirect('ministry_detail', slug=ministry.slug)
    else:
        form = MinistryMembershipForm()

    return render(request, 'ministries/join_ministry.html', {'form': form, 'ministry': ministry})

