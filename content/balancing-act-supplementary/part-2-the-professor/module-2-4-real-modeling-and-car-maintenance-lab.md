# Chapter 8. REAL Analysis Method

I couldn't keep myself from needling Eric in later classes as well. A year or so after he introduced me to the event based concepts, I took a database design class from him. I had learned Lotus 1-2-3 the prior semester, and was familiar with the “database” functions of the spreadsheet. It allowed users to select certain rows of data using criteria entered into other rows. I repeatedly pointed out these functions to Eric, and went so far as to create spreadsheet macros that demonstrated the “ability” to do all sorts of database functions. These generated a few laughs from the class when I showed them as part of our project demonstrations, but I couldn't convince Eric that a spreadsheet was a valid database.

In another class from Eric I learned how to draw pictures, but it wasn't an art class. It was a system analysis class. System analysis is the process of deciding what a computer system should do. It entails drawing system blueprints and making models of how the system will be used.

Eric suggested we should make a REAL business process model, a type of blueprint. After I graduated, Eric updated the REA acronym that McCarthy had coined to be REAL, which stands for Resource, Events, Agents, and Locations. Similar to any blueprint, the paper version can be easily changed before the real thing is constructed.

If the basic component of a building blueprint is a room, with walls, a door, and windows, the following would be the basic blueprint component of McCarthy's business process model.

<img src="../media/image27.png" style="width:3.94792in;height:2.35417in" />

*Figure 23. Standard Event Template*

The following picture shows the basic blueprint for the financial transactions we talked about in the prior chapter.

### 43

<img src="../media/image28.png" style="width:3.85417in;height:2.30208in" />

*Figure 24. Financial Event Model*

Expanding on the example in the prior chapter, financial resources are our Balance Sheet accounts and financial events are the Income Statement accounts, as well as the transfers between Balance Sheet accounts. Agents define the family members in our example system, in addition to the store or shop. The “when” is shown in dashed lines because if we simply record the date on the financial events we will have the "when" recorded.

To begin creating our blueprints, Eric suggested we start by identifying “strategically significant business activities” or events.<sup>31</sup>

**Step 1: Understand the Organization's Environment and Objectives**

This step throws the scope of what our system might do wide open. It assumes that the purpose of accounting is to provide information, and not just financial information. It goes back to the premise of Pacioli's system: accounting was the information provider for the organization. So we start by deciding what information is worth the time and cost to capture and maintain. The type of information we could gather is almost unlimited. Keeping with our family example, most every family records birth, graduation, marriage, and death dates, but we probably don't require a sophisticated system for one family's events. On the other hand, no one I know reports on washing dishes, vacuuming, doing the laundry, or mowing the lawn.

Let's assume we need financial information, so all our journals are events. So our new system has to at least do what the personal accounting system above does. From there, what other type of information do we want to capture?

Looking at our family journal entries, we have a few transactions dealing with cars. Let's assume that we really like cars, and we buy fairly expensive cars. Perhaps we also pride ourselves on maintaining our cars very well, but if we had better information about what had been done when, we could do even better.

31. Although not taught in my classes in school, Eric, working with Anita Sawyer and Owen Cherrington, developed these six steps later and documented them. Anita Sawyer Hollander, Eric L. Denna, J. Owen Cherrington, *Accounting, Information Technology, and Business Solutions*, 2nd ed. (© McGraw-Hill Companies Inc.: 2000) 46 -64.

<img src="../media/image29.jpeg" style="width:4.97917in;height:1.16667in" />

*Figure 25. Car Related Journal Entries*

So our new system is a Personal Finances and Car Maintenance Information System.

## Step 2: Identify Strategically Significant Operating Events

Do we need to record every event that deals with the car, such as when we wash it? Probably not. As we look at our car related journal entries, we can see that not every act of maintaining the car results in a journal entry. Suppose we know that we checked the oil and tire pressure during the month. But neither of those had any financial impact, so we don't have a journal entry about them. Yet, to maintain the car better, we need to know about them as well. Let's assume that we really like cars, and we buy fairly expensive cars. Perhaps we also pride ourselves on maintaining our cars very well. But if we had better information about what had been done when, we could do even better. Additionally, let's record the following events related to the car.

v Gas purchases, to track gas mileage

v Tire maintenance, including purchase and rotation

v Additional details about other maintenance

## Step 3: Analyze Each Event and Identify Resources, Agents, and Locations

So what about those events do we want to know? Eric suggested we think like a reporter.

v What happened?

v When did it occur?

v Who was involved and what roles did they play?

v What resources were involved and how much?

v Where did the event occur?

v What can go wrong during the execution of the event?

Looking at the car journal entries above, we can see that there really isn't much information about the car in the entries themselves. We know when something happened, at least the payment date. We know we used the credit card, a financial resource, and the amount. Our financial system has external and internal agents. The company name might also tell us the where—the location—at least imprecisely.

So elements of what we need to know are on the financial events. But the main thing that is missing is the car maintenance event. The journal entry documents the paying for maintenance, not maintaining the car. The only thing that gives some sense of the maintenance done is the description. And how complete is that?

Think about the receipt from the auto mechanic. The journal entry and financial event is what is at the bottom of it: the total amount. But think of all the lines on the receipt. They checked oil, filled wiper fluid, checked brake pads, rotated tires, and perhaps a host of other things. Each one of those rows might have a price on it, but we didn't record that. The events our financial system recorded were a summary of the details of maintaining the car. That is the point of what Eric was trying to teach us: the accounting view of the data precludes other uses. It leaves out information that doesn't affect the financial statements, but may be critical to the organization.

So for each car maintenance event, we are going to record: v The mileage (a form of time) at the time of maintenance v The vehicle (resource)

v Each service (resource) we are paying for

v The family member who was responsible for getting it done (internal agent)

v The shop that did the work (external agent and location)

v The date and time of the payment.

The next steps start to move us from the accounting world into the technology world; but don't take that to mean it doesn't need to be understood by the business. Similar to building a home, the homeowner still has a lot to say about what kinds of lighting will be used, and how big the shower is after the basic rooms have been designed.

## Step 4: Identify Direct Relationships Among Resources, Events, Agents, and Locations

We now move into the world of database design. To keep our explanation simple, we'll use the concept of spreadsheets to explain the next steps. Many of the basic functions of a database can be understood by someone familiar with a spreadsheet.

Similar to spreadsheets, databases are made up of tables, which usually have a set number of columns, that are “populated” with, or contain, rows of data. In our spreadsheet world, let's assume that each tab of the spreadsheet is a table. Each Resource, Event, Agent, or Location and perhaps Time would be a separate tab on the spreadsheet. We next specify the relationship between each of the tabs: Each row on one tab relates to one (1) or many (m) rows on the other tab. We end up with a picture that might look like Figure 26 on page 47:

This is an entity-relationship diagram, a very common type of ‘blueprint' for information systems. Small letters are used to indicate the relationship of the rows in the tables to the rows in other tables. For example, each car (a row in the car table) has maintenance done to it (a row in the maintenance event table), but each maintenance event only services one car. We don't record on one service event the lube for one car and check tire pressure for the other car. We represent this on the diagram as a 1 on the side of car, and an ‘m” on the side of Maintain Car events: one car is involved in many maintenance events. These numbers are called the cardinality.

Think of each box on the diagram as a tab of a spreadsheet. Each maintenance event adds a new row to the maintenance tab of the spreadsheet. But as we add new maintenance events, we don't add new cars to the cars tab of the spreadsheet. We simply have one column in the maintenance event tab that records which car (using its identifier like a car number or name) is involved in the maintenance.<sup>32</sup>

32. Linking the REA business modeling approach to an Entity Relationship Diagram is discussed in Armitage, Howard M., *Linking Management Accounting Systems with Computer Technology*, published by The Society of Management Accountants of Canada, Hamilton, Ont. \[September 1985\].

<img src="../media/image30.jpeg" style="width:5in;height:4.25in" />

*Figure 26. Process Model with Relationships*

## Step 5: Identify the REAL Relevant Behaviors, Characteristics, and Attributes

The next step in the process is to define what we want to know about each one of the boxes. This is identifying the attributes of our tables in the database, or more simply the column headings for each tab of our spreadsheet.

Suppose that below are the things we want to know about each of our Resources, Events, Agents, Location, or Time, the columns of our tables.<sup>33</sup> We'll underline the key or unique identifier for each row.

<table style="width:95%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 74%" />
</colgroup>
<thead>
<tr>
<th><strong>Entity (Table)</strong></th>
<th><strong>Attributes (Columns)</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Financial Resource</td>
<td><p><u>Financial Resource ID</u></p>
<p>Name, Bank or Credit Card Account Number, Institution Name, Contact Name</p></td>
</tr>
<tr>
<td>Car</td>
<td><p><u>Car ID</u></p>
<p>Car Name, Car Make, Car Model, Year Made, Year Purchased</p></td>
</tr>
<tr>
<td>Family Members</td>
<td><p><u>Family Member ID</u></p>
<p>Family Member Name, Birth Date, Drivers License Number</p></td>
</tr>
<tr>
<td>Shop</td>
<td><p><u>Shop ID</u></p>
<p>Shop Name, Address, Phone, Contact Name, Hours</p></td>
</tr>
<tr>
<td>Mileage</td>
<td>Mileage</td>
</tr>
</tbody>
</table>

33. Mileage and Date and Time, you can see, don't have many things to describe them. We only want to keep track of one attribute on each one of them. For this reason, we will likely simply put the mileage and the timestamp on the events themselves. Thus, in the last version of our plans, we'll make these boxes dashed boxes, meaning we are recording these things, but not in separate tables.

<table style="width:95%;">
<colgroup>
<col style="width: 20%" />
<col style="width: 74%" />
</colgroup>
<thead>
<tr>
<th><strong>Entity (Table)</strong></th>
<th><strong>Attributes (Columns)</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Date and Time</td>
<td>Timestamp</td>
</tr>
<tr>
<td>Maintain Cars</td>
<td><p><u>Maintain Event ID</u></p>
<p>ID's from other tables: Car ID, Family Member ID, Shop ID,</p>
<p>Other Attributes: Amount, Mileage and Date and Time (the actual mileage and date and time, rather than an ID, are placed right in the table)</p></td>
</tr>
<tr>
<td>Service</td>
<td><p><u>Service ID</u></p>
<p>Service Name (change oil, replace alternator, etc.), Maintenance Event ID</p></td>
</tr>
</tbody>
</table>

Defining the columns takes longer than defining the tables because there are more of them. Populating the rows takes even longer. Imagine how long it would take to type in all the values for a spreadsheet that has 10 columns, each one is about 10 characters in length, and which contains 1000 rows: That is 100,000 characters that would need to be typed. That is perhaps 10 hours of typing for an average typist.<sup>34</sup> The rows of data are really what we need to get to; they are the point of reporting.

## Results

We now have a simplified set of plans for our new information system<sup>35</sup>. This set of steps, and the resulting plans, are not that foreign to anyone who has constructed business information systems. A very similar set of diagrams, and the system built from them, could be used to build systems for manufacturing, banking, sales, and a host of others.<sup>36</sup>

Now imagine we have actually constructed the system, in a very simple way. Imagine a spreadsheet with a tab for each of the boxes, with the above column headings for each tab. Having created the spreadsheet, we have diligently captured each business event we outlined, our car maintenance events and all financial transactions for some period of time. Having captured this data, we can now query against the tables, combining them in myriad ways to produce reports.

This single system can not only generate the financial statements, it also can generate car maintenance reports. These car maintenance reports will always reconcile to the financial statements. The two types of reports can be integrated, showing costs of car maintenance, cost by car, cost by shop, and financial responsibility by family member.

The rows of data in our "spreadsheet" database are very different from the simple little financial system our accountant set up. Eric taught us, and McCarthy's paper exposed that, really there is no need for a finance system at all. In modern corporations, with modern information systems, the amount of data actually created by finance is very small compared with the data that comes from these other systems. It is, therefore, theoretically possible to gather the finance data needed from all these other systems and combine it together to produce the financial reports. The amount of data duplication is reduced; finance becomes a more relevant function as it drives a broader view of information needs in the organization; and the overall IT architecture becomes more flexible.

Having gained this understanding, my time in school was coming to a close. Such changes naturally cause reflection upon what one has learned and what one still doesn't seem to understand.

34. Assuming 33 words per minute and each word contains on average five characters.

35. Of course, many more plans are necessary to determine how data is put into these table and taken out of them to produce reports. But the premise of the theory is that capturing the appropriate data for each business event will make the these tasks much easier.

36. Kevin W. Young and Terry Magee took these concepts further in the PwC methodology Ascendant Section R0615 Event-Driven Business Modelling. See“Appendix 2: Event Driven Business Modelling” on page 335 for more information.
