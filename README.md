<mxfile host="65bd71144e">
    <diagram id="FDWRjHvNoRd4PtRVeOhn" name="实时聊天应用架构">
        <mxGraphModel dx="823" dy="473" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                <mxCell id="2" value="实时聊天应用架构" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=24;fontStyle=1" vertex="1" parent="1">
                    <mxGeometry x="360" y="20" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="3" value="React Frontend" style="swimlane;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;" vertex="1" parent="1">
                    <mxGeometry x="40" y="100" width="220" height="520" as="geometry"/>
                </mxCell>
                <mxCell id="4" value="" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
                    <mxGeometry x="50" y="120" width="200" height="20" as="geometry"/>
                </mxCell>
                <mxCell id="5" value="ChatRoom Component" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
                    <mxGeometry x="70" y="160" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="6" value="MessageList Component" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
                    <mxGeometry x="70" y="210" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="7" value="UserAuth Component" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
                    <mxGeometry x="70" y="260" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="8" value="InputBox Component" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
                    <mxGeometry x="70" y="310" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="9" value="Socket.io" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1" vertex="1" parent="1">
                    <mxGeometry x="50" y="370" width="200" height="20" as="geometry"/>
                </mxCell>
                <mxCell id="10" value="WebSocket" style="rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="120" y="410" width="60" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="11" value="Node.js Backend" style="swimlane;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#82B366;" vertex="1" parent="1">
                    <mxGeometry x="300" y="100" width="220" height="520" as="geometry"/>
                </mxCell>
                <mxCell id="12" value="API Endpoints" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
                    <mxGeometry x="310" y="120" width="200" height="20" as="geometry"/>
                </mxCell>
                <mxCell id="13" value="POST /api/auth/register" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="330" y="160" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="14" value="POST /api/auth/login" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="330" y="210" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="15" value="GET /api/rooms" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="330" y="260" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="16" value="POST /api/messages" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="330" y="310" width="160" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="17" value="Express Server" style="ellipse;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
                    <mxGeometry x="350" y="380" width="120" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="18" value="MongoDB Driver" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
                    <mxGeometry x="350" y="470" width="120" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="19" value="MongoDB" style="swimlane;whiteSpace=wrap;html=1;fillColor=#E1D5E7;strokeColor=#9673A6;" vertex="1" parent="1">
                    <mxGeometry x="560" y="100" width="220" height="520" as="geometry"/>
                </mxCell>
                <mxCell id="20" value="Collections" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
                    <mxGeometry x="570" y="120" width="200" height="20" as="geometry"/>
                </mxCell>
                <mxCell id="21" value="Users Collection { id, username, email, password }" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="590" y="160" width="160" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="22" value="Messages Collection { id, roomId, userId, content, time }" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="590" y="240" width="160" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="23" value="Rooms Collection { id, name, members[], created }" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
                    <mxGeometry x="590" y="320" width="160" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="24" value="Mongoose ODM" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
                    <mxGeometry x="610" y="420" width="120" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="25" value="" style="endArrow=classic;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="10" target="17">
                    <mxGeometry width="50" height="50" relative="1" as="geometry">
                        <mxPoint x="400" y="430" as="sourcePoint"/>
                        <mxPoint x="450" y="380" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
                <mxCell id="26" value="" style="endArrow=classic;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="18" target="24">
                    <mxGeometry width="50" height="50" relative="1" as="geometry">
                        <mxPoint x="520" y="485" as="sourcePoint"/>
                        <mxPoint x="610" y="435" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>