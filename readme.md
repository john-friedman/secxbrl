# SEC XBRL

A python package to parse sec xbrl. Supports the [datamule](https://github.com/john-friedman/datamule-python) project.

Intended to be fast & lightweight for the SEC use-case.

Other People's XBRL Packages:
* [tidyxbrl](https://github.com/cowboycodeman/tidyxbrl/)
* [brel](https://github.com/BrelLibrary/brel)
* [py-xbrl](https://github.com/manusimidt/py-xbrl/tree/main)
* [python-xbrl](https://github.com/greedo/python-xbrl)

## Installation (TODO)

## Example (TODO)
```
from secxbrl import parse_inline_xbrl, parse_xbrl
with open('inlinexbrl.html','rb') as f:
    html = f.read()

# returns a list of dictionaries (e.g. a csv)
data = parse_inline_xbrl(html)

import pandas as pd

pd.DataFrame(data).to_csv('xbrl.csv)

# and parse xbrl does the full logic using other files.
```

## How it works (working on this).

eXtensible Business Reporting Language (XBRL) is embedded in certain SEC documents, such as 10-Ks, in the form of inline XBRL.

resourcs get period, dimension, id, identifier

then we link to ix:numerci nonnumeric etc

                <ix:nonNumeric id="F_3d87f20e-1b3b-4d6f-9945-20eaa05ff33a"
                    name="us-gaap:FinanceLeaseRightOfUseAssetStatementOfFinancialPositionExtensibleList"
                    contextRef="C_e046c801-4c6a-48c1-b48f-a30525bd1ed8">
                    http://fasb.org/us-gaap/2021-01-31#PropertyPlantAndEquipmentNet</ix:nonNumeric>

--> 
{taxonomy,concept,value}

for resources need to run first then run other ix tags to extact. and link 

hmm so we should write our code using their setup, and optimize. - do want to use all files.
nah, want to do two codes
1: inline xbrl by itself
2: w/ their calc logic

for parse in line just use in html. figure out mapping
output should be 
dict with dicts inside
for nested stuff -> add _parent key

### Data Files

XBRL files submitted to the sec consist of the inline xbrl, definition, schema, label, calculation, and presentation documents.

#### Example (Tesla 10-K)

| #   | Description                                              | File                      | Type        | Size     |
|-----|----------------------------------------------------------|---------------------------|------------|---------|
| 1   | 10-K                                                     | tsla-20221231.htm         | iXBRL      | 7964288 |
| ... | ...                                                      | ...                       | ...        | ...     |
| 9   | XBRL TAXONOMY EXTENSION DEFINITION LINKBASE DOCUMENT     | tsla-20221231_def.xml     | EX-101.DEF | 550438  |
| 10  | XBRL TAXONOMY EXTENSION SCHEMA DOCUMENT                  | tsla-20221231.xsd         | EX-101.SCH | 147812  |
| 11  | XBRL TAXONOMY EXTENSION LABEL LINKBASE DOCUMENT          | tsla-20221231_lab.xml     | EX-101.LAB | 1070835 |
| 12  | XBRL TAXONOMY EXTENSION CALCULATION LINKBASE DOCUMENT    | tsla-20221231_cal.xml     | EX-101.CAL | 136183  |
| 13  | XBRL TAXONOMY EXTENSION PRESENTATION LINKBASE DOCUMENT   | tsla-20221231_pre.xml     | EX-101.PRE | 843204  |

#### Inline XBRL

Much of the inline xbrl is in the top of the document in the ix:header tag. This is hidden using a div with 'display' set to 'none'.

```<body style="margin: auto!important;padding: 8px;">
    <div style="display:none;">
        <ix:header>
            <ix:hidden> ...
            </ix:hidden>
            <ix:references>
            </ix:references>
            <ix:resources> ...
            </ix:resources>
        </ix:header>
    </div>
    ....
</body>
```

The ix:hidden tag looks like this:
```
...
<ix:nonNumeric id="F_ded02aad-d116-4cb6-9088-0a119c5d030a" name="dei:AmendmentFlag" contextRef="C_b6c8c636-658e-4c1f-97de-bb0bd181ac0d">false</ix:nonNumeric>
...
```

ix:reference provides the link to the schema document.
```
<ix:references>
    <link:schemaRef xlink:type="simple" xlink:href="tsla-20221231.xsd"></link:schemaRef>
</ix:references>
```

ix:resources
```
...
<xbrli:context id="C_e95148b7-bbbd-4e37-bd18-06e7efa3e132">
    <xbrli:entity>
        <xbrli:identifier scheme="http://www.sec.gov/CIK">0001318605</xbrli:identifier>
        <xbrli:segment>
            <xbrldi:explicitMember dimension="us-gaap:LongtermDebtTypeAxis">tsla:NonrecourseDebtMember
            </xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="us-gaap:DebtInstrumentAxis">tsla:CashEquityDebtMember
            </xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="srt:RangeAxis">srt:MinimumMember</xbrldi:explicitMember>
        </xbrli:segment>
    </xbrli:entity>
    <xbrli:period>
        <xbrli:instant>2021-12-31</xbrli:instant>
    </xbrli:period>
</xbrli:context>
...
```

Nested XBRL embedded in the document.
```
...
<ix:nonNumeric id="F_b60a7d64-ed91-418e-9389-d2096073fb4d"
contextRef="C_b6c8c636-658e-4c1f-97de-bb0bd181ac0d" name="dei:DocumentPeriodEndDate"
format="ixt:datemonthdayyearen"><span
    style="background-color:rgba(0,0,0,0);color:rgba(0,0,0,1);white-space:pre-wrap;font-weight:bold;font-size:10.0pt;font-family:&quot;Times New Roman&quot;, serif;min-width:fit-content;">December
    31, </span><span style="font-size:10.0pt;font-family:&quot;Times New Roman&quot;, serif;">
    <ix:nonNumeric id="F_b0474968-1b06-41d7-a269-885c61e06ecc"
        contextRef="C_b6c8c636-658e-4c1f-97de-bb0bd181ac0d" name="dei:DocumentFiscalYearFocus"><span
            style="background-color:rgba(0,0,0,0);color:rgba(0,0,0,1);white-space:pre-wrap;font-weight:bold;font-size:10.0pt;font-family:&quot;Times New Roman&quot;, serif;min-width:fit-content;">2022</span>
    </ix:nonNumeric>
</span></ix:nonNumeric>
...
```

XBRL embedded in the document, without nesting.
```
...
<ix:nonFraction id="F_67280f61-1793-4ac8-9e9b-9eceb6bc5ddf"
        contextRef="C_4e91897b-2f4e-40a6-af73-92666313a137"
        name="us-gaap:CashAndCashEquivalentsAtCarryingValue" unitRef="U_USD" scale="6" decimals="-6"
        format="ixt:numdotdecimal">16,253</ix:nonFraction>
...
```

