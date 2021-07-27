from transformers import BertModel,RobertaModel
import torch.nn as nn


class CustomCamemBERTModel(nn.Module):
    def __init__(self):
        super(CustomCamemBERTModel, self).__init__()

        self.bert = RobertaModel.from_pretrained("camembert-base")      
        ### New layers:
        self.dropout = nn.Dropout(0.1)
        # self.classifier = nn.Sequential(
        #     nn.Linear(768, 50),
        #     nn.ReLU(),
        #     nn.Linear(50, 3)
        # )
        self.classifier = nn.Sequential(
            nn.Linear(768, 3)
        )

          #Initialize the weights

        for module in self.children():
            if isinstance(module, nn.Linear):
                module.weight.data.normal_(mean=0.0, std=0.02)
                if module.bias is not None:
                    module.bias.data.zero_()
            elif isinstance(module, nn.Embedding):
                module.weight.data.normal_(mean=0.0, std=0.02)
                if module.padding_idx is not None:
                    module.weight.data[module.padding_idx].zero_()
            elif isinstance(module, nn.LayerNorm):
                module.bias.data.zero_()
                module.weight.data.fill_(1.0)

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        labels = None
    ):


        outputs = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        pooled_output = outputs[1]
        logits = self.classifier(pooled_output)

        # pooled_output = self.dropout(pooled_output)
        # temp_output = F.relu(self.classifier(pooled_output))
        # logits = self.classifier2(temp_output)

        loss = None

        if labels is not None:      
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, 3), labels.view(-1))

        output = (logits,) + outputs[2:]
        return ((loss,) + output) if loss is not None else output